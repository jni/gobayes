from collections import defaultdict
import networkx as nx


class IdentityDict(object):
    def __init__(self):
        pass
    def __getitem__(self, x):
        return x


def make_annotation_dict(annot_table, ontology=None, canon=IdentityDict(),
                         gene_id_column=2, annot_column=4):
    """Get a dictionary mapping genes to annotations.

    Parameters
    ----------
    annot_table : list of lists
        A gene annotation table such as that produced by
        `parsers.annotation.annotation_table`.
    ontology : NetworkX Graph, optional
        The ontology of annotation terms. See `parsers.obo.obo2networkx`. If
        provided, annotations will be traced to the root so that each
        annotation implies all its ancestors.
    canon : dict of string to string, optional
        A dictionary mapping GO IDs to canonical GO IDs. This is necessary
        when some annotations do not correspond to any node ID in the
        ontology.
    gene_id_column : int, optional
        Which column in the annotation table corresponds to Gene ID.
    annot_column : int, optional
        Which column in the annotation table corresponds to the annotation.

    Returns
    -------
    annot_dict : dict of string to list of string
        A dictionary mapping genes to ontology terms.
    """
    annot_dict = {}
    if ontology is not None:
        trace = trace_ontology(ontology)
    else:
        trace = defaultdict(list)
    for annot_row in annot_table:
        gene = annot_row[gene_id_column]
        annot = canon[annot_row[annot_column]]
        annot_dict.setdefault(gene, set([])).add(annot)
        for annot in trace[annot]:
            annot_dict[gene].add(annot)
    return annot_dict


def make_inverse_annotation_dict(annot_dict):
    inv_annot_dict = {}
    for gene, annots in annot_dict.items():
        for annot in annots:
            inv_annot_dict.setdefault(annot, set([])).add(gene)
    return inv_annot_dict


def trace_ontology(ontology):
    descendants = nx.algorithms.dag.descendants
    d = {}
    for node in ontology:
        d[node] = descendants(ontology, node)
    return d

