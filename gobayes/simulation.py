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
    """Generate a set of gene modules by sampling genes with bias.
    
    Parameters
    ----------
    gene_to_annots_map : {string: [string]} dictionary
        A map from genes (symbols, gi: accessions, etc.) to functions
        (e.g. GO ID)
    size_distribution : list of int
        The distribution of module sizes from which to sample.
    number_of_modules : int
        How many modules to generate.
    biased_annots : string or [string], optional
        Which annotations are sampled with bias. (default: None)
    bias : float, optional
        The odds of a biased annotation being chosen over an unbiased one.
        (default: 1.0, no bias).
        
    Returns
    -------
    modules : list of list of string
        A list of lists of genes selected at random.
    """
    sizes = np.random.choice(size_distribution, number_of_modules)
    modules = [generate_random_module(gene_to_annots_map, size,
        biased_annots, bias) for size in sizes]
    return modules

def convert_test_output_to_prediction(annot_to_p_value_pairs, true_annots):
    """From hypothesis test output, generate an sklearn-compatible prediction.

    sklearn and other prediction evaluation software expect prediction values
    to increase with confidence, not decrease like p-values. They also want
    a correct/incorrect label. This function takes GO hypothesis test values,
    as well as the correct annotations, and produces prediction values and
    labels.

    Parameters
    ----------
    annot_to_p_value_pairs : list of (string, float) tuples
        A one-to-one map of annotations to p-values, in tuple format.
    true_annots : list of string
        The annotations that we are actually looking for.

    Returns
    -------
    pred : float np.ndarray, shape (N,)
        The prediction values for each annotation
    y_true : int np.ndarray, shape (N,)
        Whether the prediction was true or not.
    """
    pred = []
    y_true = []
    for annot, p in annot_to_p_value_pairs:
        pred.append(-np.log10(p))
        if annot in true_annots:
            y_true.append(1)
        else:
            y_true.append(0)
    return np.array(pred), np.array(y_true)

