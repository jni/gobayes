import networkx as nx
from six.moves import map

def from_pairs(lines, elem_type=int, sep=','):
    """Return an ontology from a list of edges.

    Parameters
    ----------
    lines : iterable of string, or filename
        The input lines, two elements per line, separated by ``sep``.
    elem_type : callable or type
        The type of elements in the ontology.
    sep : string, optional
        The separator between elements on each line.

    Returns
    -------
    ont : networkx.Graph
        The ontology directed acyclic graph.
    """
    edges = (tuple(map(elem_type, line.rstrip('\n').split(sep)))
             for line in lines)
    ont = nx.from_edgelist(edges)
    return ont
