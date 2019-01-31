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


def tree_to_dot_format(tree, title, axioms, conjectures):
    edges = []

    def add_edge(root, tree):
        for subtree in tree[root]:
            child = list(subtree)[0]
            edges.append('"' + child + '"' + ' -> ' + '"' + root + '"')
            add_edge(child, subtree)
    add_edge('FALSE', tree)

    edges = list(set(edges))

    title = ['label="' + title + '"']
    style = []
    style.append('labelloc="t"')
    style.append('graph [fontname = "helvetica", fontsize=19]')
    style.append('node [fontname = "helvetica"]')
    style.append('edge [fontname = "helvetica"]')
    node_styles = []
    node_styles.append('FALSE [style=filled fillcolor=indianred1]')
    for n in axioms:
        node_styles.append(n + ' [style=filled]')
    for n in conjectures:
        node_styles.append(n + ' [style=filled fillcolor=grey50]')

    dot = ['digraph {'] + title + style + node_styles + edges + ['}']
    return '\n'.join(dot)


def draw(dot, output_name):
    if '.' in output_name:
        output_format = output_name.split('.')[-1]
    else:
        output_format = 'png'
        output_name = output_name + '.' + output_format
    dot_file = output_name.replace('.' + output_format, '.dot')
    with open(dot_file, 'w') as f:
        f.write(dot + '\n')
    format_option = '-T' + output_format
    subprocess.call(["dot", format_option, dot_file, "-o", output_name])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proof_file', type=str,
                        help="Input TPTP file with a proof to visualize.")
    parser.add_argument('output_file', type=str,
                        help="""
                        Name for the output picture. Its extension (eg. pdf or png)
                        determines a format of the output.
                        """)
    args = parser.parse_args()

    deps, axioms, conjectures = parse_tptp_proof(args.proof_file)
    tree = build_tree('FALSE', deps)
    dot = tree_to_dot_format(
        tree,
        'Proof from ' +
        args.proof_file,
        axioms,
        conjectures)
    draw(dot, args.output_file)
