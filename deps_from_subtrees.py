import sys
import argparse
import re
import subprocess
sys.path.append('.')
from proof_to_tree import parse_tptp_proof, build_tree, build_compact_tree
from proof_to_tree import statements_dict, deps_from_tree


def deps_directly_from_axioms(deps, axioms):
    axioms = set(axioms)
    deps_from_axioms = {}
    for d in deps:
        if set(deps[d]) <= axioms and len(deps[d]) > 0:
            deps_from_axioms[d] = deps[d]
    return deps_from_axioms

def root_name(tree):
    return list(tree)[0]

def subtrees_of_root(tree):
    return tree[list(tree)[0]]

def height(tree):
    subtrees = subtrees_of_root(tree)
    if len(subtrees) == 0:
        return 0
    else:
        return max([1 + height(subtree) for subtree in subtrees])

def leaves(tree):
    leaves = set()
    def add_leaves_to_list(tree0):
        if height(tree0) == 0:
            leaves.add(root_name(tree0))
        else:
            for subtree in subtrees_of_root(tree0):
                add_leaves_to_list(subtree)
    add_leaves_to_list(tree)
    return list(leaves)

def root_leaves_heigh_of_all_subtrees(tree):
    root_leaves_heigh = []
    def rlh(tree0):
        if height(tree0) > 0:
            root_leaves_heigh.append(
                (root_name(tree0), leaves(tree0), height(tree0)))
            for subtree in subtrees_of_root(tree0):
                rlh(subtree)
    rlh(tree)
    return root_leaves_heigh

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proof_file', type=str,
                        help="Input TPTP file with a proof.")
    parser.add_argument('--compact', action='store_true',
                        help="Use compacted proof trees.")
    parser.add_argument('--mode', default='root_and_leaves',
                        choices=['root_and_leaves',
                                 'theorem_and_other_leaves',
                                 'debug'],
                        help=
                        '''
                        root_and_leaves returns
                        (root_statement, leaves_names, heigh)
                        for all subtrees.
                        theorem_and_other_leaves returns
                        (theorem_statement, other_leaves_names, heigh)
                        for all subtrees.
                        ''')
    args = parser.parse_args()

    statements = statements_dict(args.proof_file)
    deps, axioms, conjectures = parse_tptp_proof(args.proof_file)
    if args.compact:
        tree = build_compact_tree('FALSE', deps)
    else:
        tree = build_tree('FALSE', deps)
    root_leaves_heigh_s = root_leaves_heigh_of_all_subtrees(tree)
    if args.mode == 'root_and_leaves':
        for rlh in root_leaves_heigh_s:
            if not statements[rlh[0]] == '$false':
                print(f'{statements[rlh[0]]}#{" ".join(rlh[1])}#{rlh[2]}')
    elif args.mode == 'theorem_and_other_leaves':
        for rlh in root_leaves_heigh_s:
            if conjectures[0] in rlh[1]:
                conj_st = statements[conjectures[0]]
                leaves_without_conj = set(rlh[1]) - set(conjectures)
                print(f'{conj_st}#{" ".join(leaves_without_conj)}#{rlh[2]}')
    else:
        for rlh in root_leaves_heigh_s:
            print(f'{rlh[0]} ## {" ".join(rlh[1])} ## {rlh[2]}')

