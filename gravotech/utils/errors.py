ERROR_TYPES = {
    "1": "Syntax error",
    "2": "Context error (invalid state)",
    "3": "Processing error",
    "4": "Authorization error",
}

ERROR_DETAILS = {
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
    if not resp.startswith("ER"):
        return resp

    parts = resp.split()

    if len(parts) < 3:
        raise ValueError(f"unable to parse this error: {resp}")

    type_err = parts[1]
    detail_err = parts[2]

    type_err_str = ERROR_TYPES.get(type_err)
    if not type_err_str:
        raise ValueError(f"error not found: {resp}")

    codes = ERROR_DETAILS.get(type_err)
    if codes is None:
        raise ValueError(f"error not found: {resp}")

    msg = codes.get(detail_err)
    if msg is None:
        raise ValueError(f"error not found: {resp}")

    error_message = f"{type_err_str}: {msg} (code: {type_err}.{detail_err})"
    return error_message
