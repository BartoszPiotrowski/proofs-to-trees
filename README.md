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

![t102_relat_1__6_premises](https://raw.githubusercontent.com/BartoszPiotrowski/proofs-to-trees/master/examples/t102_relat_1__6_premises.png?token=AJXmh8Gbu1oHr65bxw14r-UgsHwfh6smks5cXIhRwA%3D%3D)

![t123_enumset1__4_premises](https://raw.githubusercontent.com/BartoszPiotrowski/proofs-to-trees/master/examples/t123_enumset1__4_premises.png?token=AJXmh4O8JJpuXBQaGP81lIN09l-yLGXtks5cXIifwA%3D%3D)

![t100_xboole_1__12_premises](https://raw.githubusercontent.com/BartoszPiotrowski/proofs-to-trees/master/examples/t100_xboole_1__12_premises.png?token=AJXmh8FKaeBy7cf06SgOXMstiNS2UOAlks5cXIjQwA%3D%3D)
