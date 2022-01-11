"""
Utility functions for templates.
"""
from .render import get_render_context


def get_host_facts() -> dict:
    """
    Returns the facts for a single host during render. This should only be used
    within templates.

    Returns:
        dict: current host facts.
    """
    return get_render_context().get("facts", {})
