
from scipy.stats import hypergeom

def union(a, b):
    return a | b

def unions(iterable):
    return reduce(union, iterable)

def test(module, annots_dict, inverse_annots_dict, mode='standard'):
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
