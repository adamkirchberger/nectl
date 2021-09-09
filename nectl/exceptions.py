class ConfigFileError(Exception):
    """
    Indicates that errors have been encountered related to config file.
    """


class RenderError(Exception):
    """
    Indicates that render of hosts has encountered an error.
    """


class BlueprintMissingError(Exception):
    """
    Indicates that no suitable blueprint has been found for host.
    """


class BlueprintImportError(Exception):
    """
    Indicates that blueprint file does not exist or has errors.
    """
