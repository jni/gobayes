
import networkx as nx

class IdentityDict(object):
    def __init__(self):
        pass
    def __getitem__(self, x):
        return x

def make_annotation_dict(annot_table, ontology, canon=IdentityDict(),
                         trace=True, gene_id_column=2, annot_column=4):
    raw_annotations = [
        (annot_row[gene_id_column], canon[annot_row[annot_column]])
        for annot_row in annot_table]
    if trace:
        trace = trace_ontology(ontology)
        for gene, annot in raw_annotations:
            inferred = trace[annot]
            for inf_annot in inferred:
                raw_annotations.append((gene, inf_annot))
    return raw_annotations

def trace_ontology(ontology):
    descendants = nx.algorithms.dag.descendants
    d = {}
    for node in ontology:
        d[node] = descendants(ontology, node, False)
    return d
