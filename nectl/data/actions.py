class Actions:
    """
    Actions are used as type hints to tell nectl how facts should be loaded

    Examples:
        from nectl import actions

        # overwritten if defined at more specific level
        my_var: actions.replace_with = "new value"

        # merge action for lists and dictionaries
        my_var: actions.merge_with = ["appended value"]

        # frozen will hold on to the first value
        my_var: actions.frozen = "protected value"
    """

    replace_with = "replace_with"
    merge_with = "merge_with"
    frozen = "frozen"


DEFAULT_ACTION = Actions.merge_with
