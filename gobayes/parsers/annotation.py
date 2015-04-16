from __future__ import unicode_literals
import collections
import six

def annotation_table(filename, discard=[(6, 'IEA')]):
    """Return a list of lists with the full contents of a GO annotation file."""
    with open(filename, 'r') as f:
        non_header_rows = (line.rstrip('\n').split('\t') 
                            for line in f if not line.startswith('!'))
        return [r for r in non_header_rows 
                if not any([r[i] == code for i, code in discard])]

def from_pairs(lines, item_type=int, annot_type=int, sep=','):
    """Return an annotation dict from a stream of lines.

    Parameters
    ----------
    lines : iterable of string, or filename
        The lines to be parsed, of the form ``item<sep>annot``.
        A filename containing these lines will also be accepted.
    item_type : callable, optional
        The function or type used to cast the string values for the
        input items.
    annot_type : callable, optional
        The function or type used to cast the string values for the
        input annotations.
    sep : string, optional
        The separator between the item and annotation on each line.

    Returns
    -------
    annotation : dict
        A dictionary mapping items to annotations.

    Examples
    --------
    >>> lines = [['45,foo'], ['32,bar'], ['32,baz']]
    >>> from_pairs(lines, annot_type=str)
    {32: ['bar', 'baz'], 45: ['foo']}
    """
    if isinstance(lines, six.string_types):
        _open = open
    elif isinstance(lines, collections.Iterable):
        _open = lambda x: x
    else:
        raise ValueError('`lines` must be a filename or an iterable of str.')
    annotation = {}
    with _open(lines) as lines:
        for line in lines:
            item, annot = line.rstrip('\n').split(sep)
            item, annot = item_type(item), annot_type(annot)
            annotation.setdefault(item, []).append(annot)
    return annotation
