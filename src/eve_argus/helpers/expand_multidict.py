"""Helper function to expand a CIMultiDict into key-value pairs."""

from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy

type ExpandedHeaders = tuple[tuple[str, str], ...]


def expand_multi_dict(
    multidict: MultiDict[str]
    | MultiDictProxy[str]
    | CIMultiDict[str]
    | CIMultiDictProxy[str],
) -> ExpandedHeaders:
    """Convert a MultiDict-like object into a tuple of key-value pairs.

    This function takes a MultiDict (or its variants) and expands it into a tuple
    of (key, value) pairs, preserving all values for keys that appear multiple times.

    Args:
        multidict: A MultiDict-like object (MultiDict, MultiDictProxy, CIMultiDict,
            or CIMultiDictProxy) containing string keys and values.

    Returns:
        A tuple of (key, value) tuples representing all key-value
            pairs in the input multidict, including duplicate keys.

    Example:
        >>> from multidict import MultiDict
        >>> md = MultiDict([("key1", "value1"), ("key2", "value2"), ("key1", "value3")])
        >>> expand_multi_dict(md)
        (('key1', 'value1'), ('key1', 'value3'), ('key2', 'value2'))
    """
    keys = multidict.keys()
    result: list[tuple[str, str]] = []
    for key in keys:
        values = multidict.getall(key)
        for value in values:
            result.append((key, value))
    tupled_result = tuple(result)
    return tupled_result
