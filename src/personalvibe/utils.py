# Copyright © 2025 by Nick Jenkins. All rights reserved


def to_safe_name(text: str) -> str:
    """
    Converts a string into a safe, lowercase, underscore-separated name
    without using regular expressions or external imports.

    Assumes standard English characters (A–Z, a–z, 0–9, space, basic punctuation).
    """
    result = []
    for c in text:
        if c.isalnum():
            result.append(c.lower())
        elif c in ("'"):
            pass
        elif c.isspace() or c in ("-", ".", ",", "!", "?"):
            result.append("_")
        # Ignore all other characters

    # Collapse multiple underscores and strip leading/trailing ones
    safe = []
    prev = None
    for c in result:
        if c == "_" and prev == "_":
            continue
        safe.append(c)
        prev = c

    return "".join(safe).strip("_")
