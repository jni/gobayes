from collections import defaultdict
import networkx as nx

class IdentityDict(object):
    def __init__(self):
        pass
    def __getitem__(self, x):
        return x

def make_annotation_dict(annot_table, ontology=None, canon=IdentityDict(),
                         gene_id_column=2, annot_column=4):
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

def trace_ontology(ontology):
    descendants = nx.algorithms.dag.descendants
    d = {}
    for node in ontology:
        d[node] = descendants(ontology, node)
    return d
