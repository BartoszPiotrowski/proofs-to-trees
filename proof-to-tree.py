import argparse
import re
import pydot
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('proof_file', type=str)
parser.add_argument('output_file', type=str)
args = parser.parse_args()

with open(args.proof_file) as f:
    proof_lines = f.read().splitlines()

proof_lines = [l for l in proof_lines if l and not l[0] == '#']
proof_lines_words = [re.findall(r"[\w']+", l) for l in proof_lines]
#names = [l.split('(')[1].split(',')[0] for l in proof_lines]
names = [ws[1] for ws in proof_lines_words]
assert '($false)' in proof_lines[-1]
names[-1] = 'FALSE'
inputs = [names[i] for i in range(len(names)) if ' file(' in proof_lines[i]]
used = []
for ws in proof_lines_words:
    ws = ws[2:]
    us = [w for w in ws if w in names]
    used.append(us)

deps = dict(zip(names, used))
for t in deps:
    if t in inputs:
        deps[t] = []

def build_tree(start, deps):
    return {start: [build_tree(d, deps) for d in deps[start]]}

tree = build_tree('FALSE', deps)

def tree_to_dot(tree):
    edges = []
    def add_edge(root, tree):
        for subtree in tree[root]:
            child = list(subtree)[0]
            edges.append('"' + root + '"' + ' -> ' + '"' + child + '"')
            add_edge(child, subtree)
    add_edge('FALSE', tree)
    edges = list(set(edges))
    dot = ['digraph G {'] + edges + ['}']
    return '\n'.join(dot)

dot = tree_to_dot(tree)
print(dot)

def draw(dot, output_name):
    dot_file = output_name + '.dot'
    png_file = output_name + '.png'
    with open(dot_file, 'w') as f:
        f.write(dot + '\n')
    subprocess.call(["dot", "-Tpng", dot_file, "-o", png_file])

draw(dot, args.output_file)
