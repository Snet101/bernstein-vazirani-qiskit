# Bernstein–Vazirani with Qiskit

An educational implementation of the Bernstein–Vazirani algorithm, with a step-by-step notebook and automated correctness checks. Original tutorial: Sanvi Nethikunta, Team Superposition.

## Problem

Given an oracle for `f(x) = alpha · x mod 2`, recover the hidden binary string `alpha`. A deterministic classical algorithm needs `n` queries in the worst case; the ideal quantum algorithm uses one coherent oracle application. This comparison counts oracle queries, not the cost of constructing the oracle or running a classical statevector simulator.

## Run and check

From the repository root, create a Python 3.12 environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock.txt
python -m pytest -q
python scripts/check_notebook.py
```

On macOS/Linux activate with `source .venv/bin/activate` instead. The notebook command starts a fresh kernel, runs every cell, and replaces the saved notebook only after successful execution. To retain the checked-in notebook, use `python scripts/check_notebook.py --output executed.ipynb` instead. The notebook can also be opened in a notebook-capable editor using the same environment.

`requirements.txt` lists direct runtime/notebook dependencies; `requirements-dev.txt` adds test/lint tooling; `requirements.lock.txt` records the complete tested environment. The lock is a version snapshot, not a hash-locked or cross-platform verification guarantee.

## Small example

```python
from bv import input_probabilities, recover

probabilities = input_probabilities('110')
print(recover('110'))  # 110
print(sum(probabilities.values()))  # approximately 1.0
```

The complete distribution is retained. Qiskit marginalizes over the ancilla instead of slicing full-register dictionary keys, which can overwrite probability contributions.

## Files

- `bv.py`: the shared circuit builder, teaching snapshots, marginal input probabilities, and ideal recovery.
- `bernstein_vazirani.ipynb`: explanation, circuit diagrams, practice examples, and exhaustive small-case validation.
- `tests/test_bv.py`: exhaustive secrets of lengths 1–6; independent oracle-phase checks; measurement wiring; repeated calls; invalid inputs.
- `scripts/check_notebook.py`: fresh-kernel notebook execution with explicit repository working directory.
- `docs/correctness-repair.md`: original mistakes, repair decisions, validation, and scope.
- `.github/workflows/checks.yml`: automated tests, lint, and notebook execution.

## Bit ordering

Displayed `alpha` is `q_(n-1)...q_0`: its rightmost bit maps to qubit zero. The ancilla is qubit `n`. The oracle therefore iterates `reversed(alpha)`. Circuit diagrams show qubit zero at the top, while displayed outcome strings put that bit at the right. See [IBM's bit-ordering documentation](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering).

Teaching snapshots (`initialize`, `prepare`, `oracle`, `final`) come from the same implementation. The notebook does not maintain separate versions of the algorithm for its examples.

## Scope and limitations

This is **ideal local statevector simulation**, not a reproduced hardware experiment. It has no hardware job record or measured hardware runtime. Exact probabilities are not sampled shot counts; there is no shots parameter in these examples. Statevector memory scales exponentially, so the exhaustive checks deliberately use small inputs. Numerical tolerances account for floating-point error.

The oracle is constructed from a known secret for teaching and testing. This example demonstrates the oracle-query model and validates the circuit; it does not establish practical speedup or robustness to device noise.

## Contributions and repair history

The original notebook and its attribution are preserved in Git history. The correctness repair consolidates implementations, adds tests, reruns the tutorial, and corrects unsupported explanations/hardware claims. The repair was prepared with AI assistance; review and understanding of the changes are part of the project work. It is not presented as the unchanged original tutorial. See the repair note for specific findings and validation results.
