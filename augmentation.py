import sys
import argparse
import re
import subprocess
sys.path.append('.')
from proof_to_tree import parse_tptp_proof, build_tree, statements_dict

def deps_directly_from_axioms(deps, axioms, statements):
    axioms = set(axioms)
    deps_from_axioms = {}
    for d in deps:
        if set(deps[d]) <= axioms and len(deps[d]) > 0:
            deps_from_axioms[statements[d]] = deps[d]
    return deps_from_axioms

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proof_file', type=str,
                        help="Input TPTP file with a proof.")
    args = parser.parse_args()

    statements = statements_dict(args.proof_file)
    deps, axioms, _ = parse_tptp_proof(args.proof_file)
    deps = deps_directly_from_axioms(deps, axioms, statements)
    for d in deps:
        print('{}:::{}'.format(d, ' '.join(deps[d])))

