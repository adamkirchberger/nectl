from nectl.configs.render import _render_context
from nectl.configs.template_utils import get_render_facts


def test_should_return_empty_dict_when_returning_host_facts_with_default_context():
    # GIVEN that we are not running in a template and render context is blank

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to be empty dict
    assert facts == {}


def test_should_return_empty_dict_when_returning_host_facts_with_context_set():
    # GIVEN mock facts
    mock_facts = {
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN that context has been set with facts
    _render_context.set({"facts": mock_facts})

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to match mock facts
    assert facts == mock_facts

    # GIVEN that we are not running in a template and render context is blank

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to be empty dict
    assert facts == {}


def test_should_return_empty_dict_when_returning_host_facts_with_context_set():
    # GIVEN mock facts
    mock_facts = {
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN that context has been set with facts
    _render_context.set({"facts": mock_facts})

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to match mock facts
    assert facts == mock_facts
