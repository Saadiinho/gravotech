from typing import Dict

# Dictionary mapping error type codes to their human-readable category names.
# Based on the Gravotech summary table of error codes
ERROR_TYPES: Dict[str, str] = {
    "1": "Syntax error",
    "2": "Context error (invalid state)",
    "3": "Processing error",
    "4": "Authorization error",
}

# Nested dictionary providing detailed descriptions for each error type and detail code.
# Source: Technical documentation for error messages.
ERROR_DETAILS: Dict[str, Dict[str, str]] = {
    "1": {
        "1": "Unknown command",
        "2": "Not enough parameters",
        "3": "Too many parameters",
        "4": "Wrong parameter",
        "5": "Cannot open file",
        "6": "Unknown parameter",
        "7": "Wrong parameter value",
        "8": "File size limit exceeded",
        "9": "Parameter is not a string",
    },
    "2": {
        "1": "Initialization",
        "2": "CCU OK (Alive)",
        "4": "Ready to mark",
        "8": "Marking in progress",
        "16": "Pause",
        "32": "Fault",
        "state": "graveuse not in correct state",
    },
    "3": {
        "1": "Overloaded",
        "2": "Internal error TX",
        "3": "Internal error RX",
        "4": "Memory full",
        "5": "No fault to acknowledge",
        "6": "Can't acknowledge fault / Origin required",
        "7": "Stop marking is open",
        "8": "Start marking closed at power on / Out of range",
        "9": "AD failed",
    },
    "4": {
        "1": "Command reserved to the master",
    },
}


def check_err(resp: str) -> str:
    """
    Parses and decodes a raw error response from the Gravotech machine.

    This function checks if a response string begins with the "ER" prefix.
    If so, it extracts the error type and detail codes to generate a
    comprehensive human-readable error message.

    :param resp: The raw response string from the machine (e.g., "ER 1 5")
    :type resp: str

    :return: The original response if no error is detected, or a formatted
             error message (e.g., "Syntax error: Cannot open file (code: 1.5)").
    :rtype: str

    :raises ValueError: If the error response is malformed or if the codes
                        do not exist in the reference tables
    """
    if not resp.startswith("ER"):
        return resp

    # Error codes consist of 2 elements separated by a space
    parts = resp.split()

    if len(parts) < 3:
        raise ValueError(f"unable to parse this error: {resp}")

    type_err = parts[1]
    detail_err = parts[2]

    # Search for the error type category
    type_err_str = ERROR_TYPES.get(type_err)
    if not type_err_str:
        raise ValueError(f"error not found: {resp}")

    # Search for the specific error detail
    codes = ERROR_DETAILS.get(type_err)
    if codes is None:
        raise ValueError(f"error not found: {resp}")

    msg = codes.get(detail_err)
    if msg is None:
        raise ValueError(f"error not found: {resp}")

    # Format: Type Description: Detail Description (code: type.detail)
    error_message = f"{type_err_str}: {msg} (code: {type_err}.{detail_err})"
    return error_message
