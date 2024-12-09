DEPRECATION_DETECTION_ENABLED = False
CUSTOM_HTTP_DEPRECATION_HEADER = []

def is_operation_deprecated(oas: dict[str, str], path: str, method: str) -> bool:
    """
    This method checks whether an operation is deprecated, for an OpenAPI specifiaction.

    :param oas: 
        The OpenAPI specification in json format.
    :param path:
        The path of the operation. This needs the slash at the beginning.
    :param method:
        The method which is used to call this operation. It is irrelevant if it is lowercase or uppercase.

    :return:
        Returns a bool whether the operation is deprecated.
    """
    if path not in oas["paths"]:
        raise KeyError(f"Path {path} not found in the OpenAPI specification.")
    
    if method.lower() not in oas["paths"][path]:
        raise KeyError(f"Method {method.upper()} for path {path} not found in the OpenAPI specification.")
    
    if "deprecated" not in oas["paths"][path][method.lower()]:
        return False
    
    return oas["paths"][path][method.lower()]["deprecated"]

def are_parameter_deprecated(oas: dict[str, str], path: str, method: str, parameter: list[str]) -> tuple[bool, list[str]]:
    """
    This method checks whether any parameter of an operation are deprecated, for an OpenAPI specifiaction.

    :param oas: 
        The OpenAPI specification in json format.
    :param path:
        The path of the operation. This needs the slash at the beginning.
    :param method:
        The method which is used to call this operation. It is irrelevant if it is lowercase or uppercase.
    :param parameter:
        The parameter which are used to call this operation.

    :return:
        Returns a tuple containing a bool whether parameter are deprecated and a list of parameter that are deprecated.
    """
    if path not in oas["paths"]:
        raise KeyError(f"Path {path} not found in the OpenAPI specification.")
    
    if method.lower() not in oas["paths"][path]:
        raise KeyError(f"Method {method.upper()} for path {path} not found in the OpenAPI specification.")
    
    if "parameters" not in oas["paths"][path][method.lower()]:
        raise KeyError(f"No parameters found for {path} with method {method.upper()} in the OpenAPI specification.")
    
    deprecatedParams = []
    for parameter_object in oas["paths"][path][method.lower()]["parameters"]:
        if "deprecated" in parameter_object and parameter_object["deprecated"] and parameter_object["name"] in parameter and parameter_object["in"] == "query":
            deprecatedParams.append(parameter_object["name"])
    
    return (deprecatedParams != [], deprecatedParams)

def set_deprecation_http_header(http_header: list[str]) -> None:
    """
    Set the header fields that should be used to detect deprecation. "sunset" and "deprecation" are always used.

    :param http_header: A list of header names that should be used.
    """
    global CUSTOM_HTTP_DEPRECATION_HEADER
    CUSTOM_HTTP_DEPRECATION_HEADER = http_header

def add_deprecation_http_header(http_header: list[str]) -> None:
    """
    Add header fields, to existing ones that should be used to detect deprecation. "sunset" and "deprecation" are always used.

    :param http_header: A list of header names that should be used and extend the already existing ones.
    """
    global CUSTOM_HTTP_DEPRECATION_HEADER 
    CUSTOM_HTTP_DEPRECATION_HEADER.extend(http_header)

def deprecation_detection(enabled: bool) -> None:
    """
    Enables or disables the deprecation detection.

    :param enabled: Boolean whether or not the deprecation detection should be performed.
    """
    global DEPRECATION_DETECTION_ENABLED
    DEPRECATION_DETECTION_ENABLED = enabled

def get_deprecation_detection() -> bool:
    """
    Returns whether deprecation detection is enabled or not.
    """
    global DEPRECATION_DETECTION_ENABLED
    return DEPRECATION_DETECTION_ENABLED

def get_deprecation_http_header() -> list[str]:
    """
    Returns header fields that should be used to detect deprecation. "sunset" and "deprecation" are always used.
    """
    global CUSTOM_HTTP_DEPRECATION_HEADER 
    return CUSTOM_HTTP_DEPRECATION_HEADER
