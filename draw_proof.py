import sys
import argparse
import subprocess
sys.path.append('.')
from proof_to_tree import parse_tptp_proof, build_tree, build_compact_tree


def tree_to_dot_format(tree, title, axioms, conjectures):

    edges = []

    def add_edge(root, tree):
        for subtree in tree[root]:
            child = list(subtree)[0] # subtree is a dict with one element
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
                        Name for the output picture. Its extension (eg. pdf or
                        png) determines format of the output.
                        """)
    parser.add_argument('--compact', action='store_true',
                        help="Draw compact tree with removed intermediate steps.")
    args = parser.parse_args()

    deps, axioms, conjectures = parse_tptp_proof(args.proof_file)
    if args.compact:
        tree = build_compact_tree('FALSE', deps)
    else:
        tree = build_tree('FALSE', deps)
    dot = tree_to_dot_format(
        tree,
        'Proof from ' +
        args.proof_file,
        axioms,
        conjectures)
    draw(dot, args.output_file)
