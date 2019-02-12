import re


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


def build_compact_tree(start, deps):
    def bct(s):
        if len(deps[s]) == 1:
            return bct(deps[s][0])
        else:
            return {s: [bct(d) for d in deps[s]]}
    return bct(start)


def statements_dict(proof_file):
    with open(proof_file) as f:
        proof_lines = f.read().splitlines()
    proof_lines = [l for l in proof_lines if l and not l[0] == '#']
    proof_lines = [l.replace(' ','') for l in proof_lines]
    proof_lines_cut = [','.join(l.split(',')[2:]) for l in proof_lines]
    # TODO shorten below
    proof_lines_words = [re.findall(r"[\w']+", l) for l in proof_lines]
    names = [ws[1] for ws in proof_lines_words]
    assert '($false)' in proof_lines[-1]
    names[-1] = 'FALSE'
    ###
    statements = []
    for l in proof_lines_cut:
        if ',file(' in l:
            statements.append(l.split(',file(')[0])
        else:
            statements.append(l.split(',inference(')[0])
    for i in range(len(statements)):
        if statements[i][0] == '(':
            statements[i] = statements[i][1:-1]
    assert len(statements) == len(proof_lines) == len(names)
    statements_dict = {names[i]: statements[i] for i in range(len(names))}
    return statements_dict

