# Correctness repair — October 15, 2026

Baseline commit: `1b07beaedc6037e60743acb85c03dfc436361571`.
Original notebook attribution: Sanvi Nethikunta, Team Superposition.

## Problems in the baseline

- Full-register probability keys were shortened with a dictionary comprehension, overwriting ancilla contributions rather than summing them. The saved main example's probability mass was approximately 0.5.
- The practice section created a new state but read `probs` from an earlier example.
- Different oracle examples used different string-to-qubit conventions; the local test extracted the wrong register bits. A single convenient passing string did not establish correctness.
- The classical example assumed an unqueried bit was zero, although two candidate secrets matched the observations.
- The explanation called a single-qubit minus state a Bell state and mischaracterized the role of entanglement.
- Commented submission code and unsupported prose claimed hardware deployment and short runtimes without a saved hardware job record.
- The final example discarded other outcomes instead of checking the complete distribution. A prose exercise discussed shots although its code computed exact statevector probabilities.

## Design choices

1. One `build_bv` implementation, with optional teaching snapshots. `alpha` is displayed `q_(n-1)...q_0`, so the rightmost secret bit maps to qubit zero. Snapshot branches expose initialization, preparation, and oracle stages without independent circuit implementations.
2. Qiskit's input-register marginal probability API sums out the ancilla. Complete distributions are retained for validation; no max-only filtering is used to hide residual outcomes.
3. Fresh circuits/states on each call eliminate notebook state reuse. The notebook has been reorganized into a coherent tutorial instead of preserving repeated, inconsistent examples.
4. Independent oracle-phase tests derive amplitudes from the classical parity formula, rather than merely comparing two wrappers around the same circuit builder.
5. Hardware execution is a clearly labeled future extension. No credentials, hardware jobs, or empirical runtimes are claimed. Statevector simulation does not establish a practical quantum speedup.
6. Dependencies match the demonstrated statevector/notebook workflow. Unused Aer and obsolete hardware-provider examples were removed. A recorded environment and CI recipe support repeatable checks.

## Validation

See the accompanying validation report for the actual commands, environment, and results. Required checks are: pytest, Ruff, and top-to-bottom execution from a fresh kernel. Tests cover all 126 secrets of lengths 1–6, probability normalization, oracle phases, measurement wiring, teaching snapshots, repeated examples, and invalid inputs. Linux CI is configured separately; local Windows results do not establish that a remote workflow has passed.

## Scope and attribution

This is a new correctness repair, prepared with AI assistance, not a claim that these tests or explanations existed in the original submission. Original files remain available in baseline Git history. No hardware execution or large-input validation is included. A user should review and understand the changes before using this project as an application sample.

## Reference

[IBM Qiskit bit-ordering guide](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering).
