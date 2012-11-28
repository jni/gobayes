import numpy as np

def generate_random_module(gene_to_annots_map, size,
                           biased_annots=None, bias=1.0):
    """Produce a gene module by biased sampling of a specific annotation.

    Parameters
    ----------
    gene_to_annots_map : {string: [strings]} dictionary
        A map from genes (symbols, gi: accessions, etc.) to functions
        (e.g. GO ID).
    size : int
        The number of genes in the module
    biased_annot : string or [string], optional
        Which annotation to produce a sampling bias for. 
        (default: None)
    bias : float, optional
        How much more likely the biased annotation is to be chosen
        rather than some other annotation. (default: 1.0, no bias)

    Returns
    -------
    module : list of strings
        A list of genes selected at random (either uniformly or biased)
    """
    genes = gene_to_annots_map.keys()
    p = np.ones(len(genes))
    if biased_annots is not None:
        if type(biased_annots) == str:
            biased_annots = [biased_annots]
        for i, gene in enumerate(genes):
            if any([biased_annot in gene_to_annots_map[gene]
                                    for biased_annot in biased_annots]):
                p[i] = bias
    p /= p.sum()
    module = list(np.random.choice(genes, size, replace=False, p=p))
    return module

def generate_multiple_modules(gene_to_annots_map, size_distribution,
                              number_of_modules, biased_annots=None, bias=1.0):
    """Generate a set of gene modules by sampling genes with bias."""
    sizes = np.random.choice(size_distribution, number_of_modules)
    modules = [generate_random_module(gene_to_annots_map, size,
        biased_annots, bias) for size in sizes]
    return modules
