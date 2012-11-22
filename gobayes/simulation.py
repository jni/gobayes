import numpy as np

def generate_random_module(gene_to_annots_map, size,
                           biased_annot=None, bias=1.0):
    """Produce a gene module by biased sampling of a specific annotation.

    Parameters
    ----------
    gene_to_annots_map : {string:[strings]} dictionary
        A map from genes (symbols, gi: accessions, etc.) to functions
        (e.g. GO ID).
    size : int
        The number of genes in the module
    biased_annot : string, optional
        Which annotation to produce a sampling bias for. 
        (default: None)
    bias : float, optional
        How much more likely the biased annotation is to be chosen
        rather than some other annotation. (default: 1.0, no bias)
    """
    genes = gene_to_annots_map.keys()
    p = np.ones(len(genes))
    for i, gene in enumerate(genes):
        if biased_annot in gene_to_annots_map[gene]:
            p[i] = bias
    return list(np.random.choice(genes, size, replace=False, p=p))
