# Local validation — October 15, 2026

Baseline: `1b07beaedc6037e60743acb85c03dfc436361571`.

Environment: newly created Windows virtual environment, Python 3.12.14, Qiskit 2.5.2. Complete installed versions are recorded in `requirements.lock.txt`.

| Check | Result |
|---|---|
| Dependency consistency (`python -m pip check`) | Passed: no broken requirements |
| Unit/circuit checks (`python -m pytest -q`) | 143 tests passed |
| Lint (`python -m ruff check .`) | Passed |
| Fresh-kernel notebook (`python scripts/check_notebook.py`) | Passed; process exit code 0 |
| Saved notebook execution | All 11 code cells executed in order, no error outputs |
| Saved figures | Five circuit diagrams and three histograms (8 PNGs) |
| Representative figure inspection | Main measurement circuit, 110 histogram, and 1011 histogram inspected |

The tests include all 126 binary secrets of lengths one through six, normalized input-register probabilities, expected secret recovery, independently derived oracle-phase amplitudes, measurement wiring, teaching snapshots, repeated examples, and invalid inputs. The notebook also asserts all 126 cases during its own clean-kernel run.

The first headless run produced no saved charts; explicit inline rendering and an eight-figure output check now catch that failure. A Windows ZeroMQ event-loop shutdown problem was resolved by selecting the supported Windows selector event loop before notebook execution; the final command exited successfully.

The environment was installed fresh from direct dependencies before generating the lock snapshot. That exact lock was not installed into a second independent environment. Linux GitHub Actions is configured but has not been run remotely yet. No hardware job, noisy-device benchmark, or large-input performance claim is included.
