import itertools as it

import networkx as nx

def is_stanza_name(string):
    return string.startswith('[') and string.endswith(']')

def is_transitive_relationship(typedef):
    return (typedef.has_key('is_transitive') and
            typedef['is_transitive'][0] == 'true')

def obo2networkx(filename, parent_relationships=['is_a', 'part_of']):
    """Build a graph from an OBO file."""
    header, stanzas = parse_obo_raw(filename)
    terms = stanzas['Term']
    g = nx.DiGraph()
    g.add_nodes_from([term['id'] for term in terms])
    for term in terms:
        g.node[term['id']].update(term)
        for rel in parent_relationships:
            if term.has_key(rel):
                for parent in term[rel]:
                    g.add_edge(term['id'], parent['id'], kind=rel)
    return g

def canonical_go_id(filename):
    """Return a mapping from synonymous GO IDs to their canonical ID.
    
    The Gene Ontology (GO) database maps more than one GO ID to the same GO
    term, probably for historical reasons. These appear as entries in a GO
    term stanza with the key `alt_id`.
    
    This function returns a Python dictionary mapping any ID to the
    canonical GO ID, that is, the one appearing under the `id` key in the
    OBO file.

    Parameters
    ----------
    filename : str
        The name of the Gene Ontology OBO flat file.

    Returns
    -------
    d : dict
        A python dictionary mapping IDs to canonical IDs.
    """
    terms = parse_obo_raw(filename)[1]['Term']
    d = {}
    for term in terms:
        term_id = term['id']
        d[term_id] = term_id
        if term.has_key('alt_id'):
            for alt_id in term['alt_id']:
                d[alt_id] = term_id
    return d

def parse_obo_raw(filename):
    """Parse an OBO file into list of stanzas."""
    with open(filename, 'r') as f:
        lines_iter = (line.rstrip('\n') for line in f if line != '\n')
        lines_iter = it.groupby(lines_iter, is_stanza_name)
        lines_iter = (group[1] for group in lines_iter)
        header = get_header(lines_iter)
        stanzas = get_stanzas(lines_iter)
    return header, stanzas

def get_header(lines_iter):
    """Return header dictionary and remove corresponding lines from input."""
    header = {}
    header_lines = lines_iter.next()
    for line in header_lines:
        key, value = line.split(': ', 1)
        if header.has_key(key):
            existing_value = header[key]
            if type(existing_value) != list:
                header[key] = [existing_value, value]
            else:
                existing_value.append(value)
        else:
            header[key] = value
    return header

def get_stanzas(lines_iter):
    """Return keyed lists of stanzas from OBO lines cleaned of the header."""
    stanzas = {}
    while True:
        try:
            stanza_name, stanza = pop_stanza(lines_iter)
            stanzas.setdefault(stanza_name, []).append(stanza)
        except StopIteration:
            break
    return stanzas

def pop_stanza(lines_iter):
    stanza = {}
    stanza_name = lines_iter.next().next()[1:-1]
    stanza_lines = lines_iter.next()
    for line in stanza_lines:
        key, value = line.split(': ', 1)
        if len(value.split(' ! ')) > 1:
            value_id, value_name = value.split(' ! ', 1)
            value = {'id': value_id, 'name': value_name}
        if key == 'id' or key == 'name':
            stanza[key] = value
        else:
            stanza.setdefault(key, []).append(value)
    return stanza_name, stanza
