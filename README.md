# Simple tool for visualizing TPTP proofs

## Usage

Having a proof in TPTP format, for instance `proofs/t123_enumset1__4_premises.tptp`
'(which is output from `E` prover) you can run

```
python3 proof-to-tree.py proofs/t123_enumset1__4_premises.tptp examples/t123_enumset1__4_premises.pdf
```

First argument to the `proof-to-tree.py` script is input path, second is output path.
This produces two files: `examples/t123_enumset1__4_premises.dot` and
`examples/t123_enumset1__4_premises.pdf`. The first file contains specification of a graph
in DOT language, whereas the second file is visualization of this graph
produced by `Graphviz` package.

You can give another extension to the output, for instane `.png` instead of
`.pdf` and the script should respect it.

## Examples



