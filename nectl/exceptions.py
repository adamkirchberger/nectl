class DiscoveryError(Exception):
    """
    Indicates that an error has been encountered during data tree discovery.
    """


class ConfigFileError(Exception):
    """
    Indicates that errors have been encountered related to config file.
    """


class RenderError(Exception):
    """
    Indicates that render of hosts has encountered an error.
    """


class TemplateMissingError(Exception):
    """
    Indicates that no suitable template has been found for host.
    """


class TemplateImportError(Exception):
    """
    Indicates that template file does not exist or has errors.
    """
