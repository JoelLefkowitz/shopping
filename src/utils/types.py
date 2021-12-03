from typing import Any, Dict


def dict_matches_type(dct: Dict[Any, Any], keys: Any, values: Any) -> bool:
    """
    >>> dict_matches_type({"a": 1}, str, int)
    True

    >>> dict_matches_type({"a": "1"}, str, int)
    False
    """
    return all(
        [
            *[isinstance(x, keys) for x in dct],
            *[isinstance(x, values) for x in dct.values()],
        ]
    )
