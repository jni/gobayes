from __future__ import unicode_literals

def annotation_table(filename, discard=[(6, 'IEA')]):
    """Return a list of lists with the full contents of a GO annotation file."""
    with open(filename, 'r') as f:
        non_header_rows = (line.rstrip('\n').split('\t') 
                            for line in f if not line.startswith('!'))
        return [r for r in non_header_rows 
                if not any([r[i] == code for i, code in discard])]

