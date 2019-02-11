import sys
import argparse
import re
import subprocess


def parse_tptp_proof(proof_file):
    with open(proof_file) as f:
        proof_lines = f.read().splitlines()

    proof_lines = [l for l in proof_lines if l and not l[0] == '#']
    proof_lines_words = [re.findall(r"[\w']+", l) for l in proof_lines]
    names = [ws[1] for ws in proof_lines_words]
    assert '($false)' in proof_lines[-1]
    names[-1] = 'FALSE'
    axioms = [names[i]
              for i in range(len(names)) if 'axiom' in proof_lines_words[i]]
    conjectures = [
        names[i] for i in range(
            len(names)) if 'conjecture' in proof_lines_words[i]]
    used = []
    for ws in proof_lines_words:
        ws = ws[2:]
        us = [w for w in ws if w in names]
        used.append(us)

    deps = dict(zip(names, used))
    for t in deps:
        if t in axioms or t in conjectures:
            deps[t] = []
    return deps, axioms, conjectures


def build_tree(start, deps):
    return {start: [build_tree(d, deps) for d in deps[start]]}
