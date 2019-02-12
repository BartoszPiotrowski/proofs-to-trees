# Simple tool for visualizing TPTP proofs

## Requirements
`Python 3` and `Graphviz`.

## Usage

Having a proof in TPTP format, for instance [proofs/t123_enumset1__4_premises.tptp](https://github.com/BartoszPiotrowski/proofs-to-trees/blob/master/proofs/t123_enumset1__4_premises.tptp)
(which comes from `E` prover) you can run:

```
python3 draw_proof.py proofs/t123_enumset1__4_premises.tptp examples/t123_enumset1__4_premises.pdf
```

First argument to the `draw_proof.py` script is an input path, second is an output path.
This produces two files: `examples/t123_enumset1__4_premises.dot` and
`examples/t123_enumset1__4_premises.pdf`. The first file contains a specification of a graph
in DOT language, whereas the second file is a visualization of this graph
produced by `Graphviz` package.

You can give another extension to the output, for instance `.png` instead of
`.pdf` and the script should respect it.

Axioms used in the proof will be marked by light-grey color and a conjecure
will be coloured darker.

There is also an option of drawing "compacted" proof trees, where intermediate
nodes being the only parent of its children are removed. You can activate this
option via the `--compact` flag:

```
python3 draw_proof.py proofs/t123_enumset1__4_premises.tptp examples/t123_enumset1__4_premises.pdf --compact True
```

## Examples


![t123_enumset1__4_premises](https://raw.githubusercontent.com/BartoszPiotrowski/proofs-to-trees/master/examples/t123_enumset1__4_premises.png?token=AJXmh4O8JJpuXBQaGP81lIN09l-yLGXtks5cXIifwA%3D%3D)



![t102_relat_1__6_premises](https://raw.githubusercontent.com/BartoszPiotrowski/proofs-to-trees/master/examples/t102_relat_1__6_premises.png?token=AJXmh8Gbu1oHr65bxw14r-UgsHwfh6smks5cXIhRwA%3D%3D)



![t100_xboole_1__12_premises](https://raw.githubusercontent.com/BartoszPiotrowski/proofs-to-trees/master/examples/t100_xboole_1__12_premises.png?token=AJXmh8FKaeBy7cf06SgOXMstiNS2UOAlks5cXIjQwA%3D%3D)
