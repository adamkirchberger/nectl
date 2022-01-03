import time
from typing import Sequence, Dict, Any
import inspect
from contextlib import redirect_stdout
from contextvars import ContextVar
import io

from ..logging import get_logger
from ..config import Config, get_config
from ..exceptions import (
    TemplateImportError,
    TemplateMissingError,
    RenderError,
)
from ..data.hosts import Host
from .templates import Template, get_template


logger = get_logger()
_render_context: ContextVar[Dict] = ContextVar("render_context", default={})


def get_host_facts() -> dict:
    """
    Returns the current host facts, this should only be used within templates.

    Returns:
        dict: current host facts.
    """
    return _render_context.get().get("facts", {})


def render_hosts(hosts: Sequence[Host], config: Config = None) -> Dict[str, Any]:
    """
    Returns rendered configs for hosts using templates which are matched based
    on the 'os_name' value.

    Args:
        hosts (List[Host]): hosts to render templates for.
        config (Config): config settings.

    Returns:
        Dict[str,Any]: dict with item per host with rendered template.

    Raises:
        RenderError: if there are issues with templates.
    """
    config = get_config() if config is None else config

    results = {}

    ts_start = time.perf_counter()
    logger.debug("start rendering templates")

    for host in hosts:
        if host.os_name is None or host.os_version is None:
            logger.info(
                f"skipping host render with no 'os_name' or 'os_version': {host.id}"
            )
            continue

        logger.debug(f"{host.id}: setting render context")
        _render_context.set({"facts": host.facts})  # set host facts

        try:
            # Get matching template
            template = get_template(os_name=host.os_name, config=config)

            # Render template and add to results
            results[host.id] = render_template(template, host.facts)

        except (TemplateMissingError, TemplateImportError) as e:
            raise RenderError(str(e)) from e
        finally:
            logger.debug(f"{host.id}: clearing render context")
            _render_context.set({})  # set context to empty dict

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished rendering templates ({dur}s)")

    return results


def render_template(template: Template, facts: Dict[str, Any]) -> str:
    """
    Returns rendered configuration for host facts using supplied template.

    Args:
        template: Template class.
        facts (Dict[str,Any]): host facts.

    Returns:
        rendered host configuration.

    Raises:
        RenderError: if there are issues during render.
    """
    ts_start = time.perf_counter()
    host_id = facts.get("id")
    logger.debug(f"{host_id}: starting render")

    template_name = getattr(template, "__name__")
    logger.info(f"{host_id}: using template '{template_name}'")

    logger.debug(f"{host_id}: collecting template sections")
    sections = {
        name: func
        for name, func in template.__dict__.items()
        if callable(func) and not name.startswith("_")
    }
    logger.debug(
        f"{host_id}: found {len(sections)} template sections: {list(sections.keys())}"
    )

    out = []
    errors = 0  # error counter used to only alert at the end

    # Loop through each template section
    for sname, section in sections.items():
        logger.info(f"{host_id}: rendering template: {template_name}:{sname}")
        try:
            # Get args that template needs
            args = {}
            for arg_name, arg in inspect.signature(section).parameters.items():
                # Optional args which have default values
                if arg.default is not arg.empty:
                    args[arg_name] = facts.get(arg_name, arg.default)
                # Required args which will raise error when not in facts
                else:
                    args[arg_name] = facts[arg_name]

            # Render template section
            with redirect_stdout(io.StringIO()) as f:
                # Capture section print statements
                section(**args)

            render = f.getvalue()  # assign output
            render = render.strip("\n")  # strip empty newline at end

        except KeyError as e:
            # Catch missing facts errors
            logger.critical(
                f"{host_id}: template '{template_name}:{sname}' "
                f"needs fact: {str(e)}"
            )
            errors += 1  # increase errors counter
            continue  # move to next template section
        except Exception as e:
            # Catch all other errors
            logger.critical(
                f"{host_id}: template '{template_name}:{sname}' unknown error: {e}"
            )
            logger.exception(e)
            errors += 1  # increase errors counter
            continue  # move to next template section
        out.append(render)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"{host_id}: finished render ({dur}s)")

    if errors:
        msg = f"render aborted due to {errors} render errors with host: {host_id}"
        logger.critical(msg)
        raise RenderError(msg)

    return "\n".join(out)
