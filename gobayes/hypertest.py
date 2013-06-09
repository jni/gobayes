from scipy.stats import hypergeom


def union(a, b):
    return a | b


def unions(iterable):
    """Compute the set union of all items in a list.

    Parameters
    ----------
    iterable : any iterable
        A list/tuple/generator of elements supporting set union.

    Returns
    -------
    s : set
        A set of all the items represented within iterable.
    """
    return reduce(union, iterable)


def test(module, annots_dict, inverse_annots_dict, mode='standard'):
    """Use the hypergeometric test on functions in a gene module.

    The hypergeometric test is also known as Fisher's exact test.

    Parameters
    ----------
    module : [string]
        The list of genes in a module.
    annots_dict : {string: [string]} dictionary
        A mapping of genes to functions
    inverse_annots_dict : {string: [string]} dictionary
        A mapping of functions to genes
    mode : {'standard', 'conditional'}, optional
        Whether to use the standard hypergeometric test or the conditional one
        (default: standard).

    Returns
    -------
    d : {string: float} dictionary
        A mapping of functions to p-values.
    """
    represented_functions = unions([annots_dict[gene] for gene in module])
    d = {}
    num_genes = len(annots_dict)
    num_drawn = len(module)
    for function in represented_functions:
        num_labeled_total = len(inverse_annots_dict[function])
        num_labeled_in_module = sum(
                            [function in annots_dict[gene] for gene in module])
        d[function] = hypergeom.sf(num_labeled_in_module - 1, num_genes,
                                   num_labeled_total, num_drawn)
        if mode.startswith('c'):
            d[function] /= hypergeom.sf(0, num_genes, num_labeled_total, 
                                        num_drawn)
    return d

