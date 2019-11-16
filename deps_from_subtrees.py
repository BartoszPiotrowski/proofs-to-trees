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
        if not subtrees_of_root(tree0):
            leaves.add(root_name(tree0))
        else:
            for subtree in subtrees_of_root(tree0):
                add_leaves_to_list(subtree)
    add_leaves_to_list(tree)
    return list(leaves)

def root_leaves_heigh_of_all_subtrees(tree):
    root_leaves_heigh = []
    def rlh(tree0):
        h = height(tree0)
        if h > 0:
            root_leaves_heigh.append((root_name(tree0), leaves(tree0), h))
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
                                 'root_and_axioms',
                                 'conj_and_other_leaves',
                                 'debug'],
                        help=
                        '''
                        root_and_leaves returns
                        (root_statement, leaves_names, heigh)
                        for all subtrees, leaves DO contain a conjecture.
                        root_and_axioms returns
                        (root_statement, leaves_names, heigh)
                        for all subtrees, leaves DO NOT contain a conjecture.
                        conj_and_other_leaves returns
                        (conjecture_statement, other_leaves_names, heigh)
                        for all subtrees.
                        ''')
    args = parser.parse_args()

    statements = statements_dict(args.proof_file)
    deps, axioms, conjectures = parse_tptp_proof(args.proof_file)
    #print(axioms); sys.exit()
    assert len(conjectures) == 1
    conjecture = conjectures[0]
    if args.compact:
        tree = build_compact_tree('FALSE', deps)
    else:
        tree = build_tree('FALSE', deps)
    root_leaves_heigh_s = root_leaves_heigh_of_all_subtrees(tree)
    if args.mode == 'root_and_leaves':
        for rlh in root_leaves_heigh_s:
            root_st = statements[rlh[0]]
            # intersection with axioms because of, e.g. introduction(definition)
            # in the proofs -- leave which is not an axiom
            leaves = set(rlh[1]).intersection(set(axioms))
            leaves = sorted(leaves)
            if not root_st == '$false':
                print(f'{root_st}#{" ".join(leaves)}#{rlh[2]}')
    elif args.mode == 'root_and_axioms':
        for rlh in root_leaves_heigh_s:
            if not conjecture in rlh[1]:
                root_st = statements[rlh[0]]
                leaves = set(rlh[1]).intersection( set(axioms) | {conjecture} )
                leaves = sorted(leaves)
                print(f'{root_st}#{" ".join(leaves)}#{rlh[2]}')
    elif args.mode == 'conj_and_other_leaves':
        for rlh in root_leaves_heigh_s:
            if conjecture in rlh[1]:
                conj_st = statements[conjecture]
                leaves = set(rlh[1]).intersection(set(axioms))
                leaves_without_conj = leaves - {conjecture}
                leaves_without_conj = sorted(leaves_without_conj)
                print(f'{conj_st}#{" ".join(leaves_without_conj)}#{rlh[2]}')
    else:
        for rlh in root_leaves_heigh_s:
            print(f'{rlh[0]} ## {" ".join(rlh[1])} ## {rlh[2]}')

