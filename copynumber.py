"""
Generate copynumber.json from sequences.json

Usage:
copynumber.py <infile> <outfile>

"""

import json
import sys

def run(infile, outfile):
    seqs = json.load(open(infile))
    keys = seqs.keys() - ['MRCA', 'Combined']
    names = list(seqs[k]['Observed'].keys() for k in keys)
    names = set().union(*names)
    result = dict((n, int(n.split('_')[3])) for n in names)
    json.dump(result, open(outfile, 'w'))


if __name__ == "__main__":
    infile, outfile = sys.argv[1:]
    run(infile, outfile)
