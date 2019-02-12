import sys
import argparse
import re
import subprocess
sys.path.append('.')
from proof_to_tree import parse_tptp_proof, build_compact_tree
from proof_to_tree import statements_dict, deps_from_tree


def deps_directly_from_axioms(deps, axioms):
    axioms = set(axioms)
    deps_from_axioms = {}
    for d in deps:
        if set(deps[d]) <= axioms and len(deps[d]) > 0:
            deps_from_axioms[d] = deps[d]
    return deps_from_axioms

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proof_file', type=str,
                        help="Input TPTP file with a proof.")
    parser.add_argument('--compact', action='store_true',
                        help="Use compacted proof trees.")
    args = parser.parse_args()

    statements = statements_dict(args.proof_file)
    deps, axioms, _ = parse_tptp_proof(args.proof_file)
    if args.compact:
        compact_tree = build_compact_tree('FALSE', deps)
        deps = deps_from_tree(compact_tree)
        for d in deps:
            print('{}#{}'.format(statements[d], ' '.join(deps[d])))
    else:
        deps = deps_directly_from_axioms(deps, axioms)
        for d in deps:
            print('{}#{}'.format(statements[d], ' '.join(deps[d])))

