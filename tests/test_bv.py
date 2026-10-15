"""Small exhaustive cases catch reversals, stale state, and lost probability."""
from itertools import product

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from bv import build_bv, input_probabilities, recover

STRINGS = ["".join(bits) for n in range(1, 7) for bits in product("01", repeat=n)]


@pytest.mark.parametrize("alpha", STRINGS)
def test_complete_input_distribution_and_recovery(alpha):
    probabilities = input_probabilities(alpha)
    assert sum(probabilities.values()) == pytest.approx(1.0, abs=1e-12)
    assert probabilities[alpha] == pytest.approx(1.0, abs=1e-12)
    assert all(len(key) == len(alpha) for key in probabilities)
    assert recover(alpha) == alpha


@pytest.mark.parametrize("alpha", ["001", "110", "1011", "100001"])
def test_measured_circuit_matches_unmeasured_distribution(alpha):
    measured = build_bv(alpha, measure=True)
    measurements = [(item.qubits[0], item.clbits[0]) for item in measured.data
                    if item.operation.name == "measure"]
    assert measurements == list(zip(measured.qubits[:len(alpha)], measured.clbits))
    state = Statevector.from_instruction(measured.remove_final_measurements(inplace=False))
    assert state.probabilities_dict(qargs=list(range(len(alpha))))[alpha] == pytest.approx(1)


@pytest.mark.parametrize("alpha", ["001", "110", "1011"])
def test_oracle_snapshot_matches_independent_phase_formula(alpha):
    n = len(alpha)
    secret = int(alpha, 2)
    # Basis index x + ancilla*2**n; ancilla stays in |minus> after phase kickback.
    expected = np.array([
        (-1) ** ((secret & x).bit_count() + ancilla) / np.sqrt(2 ** (n + 1))
        for ancilla in (0, 1) for x in range(2**n)
    ])
    actual = Statevector.from_instruction(build_bv(alpha, stage="oracle"))
    np.testing.assert_allclose(actual.data, expected, atol=1e-12)


def test_teaching_initialization_and_preparation():
    initialized = Statevector.from_instruction(build_bv("110", stage="initialize"))
    assert initialized.probabilities_dict()["1000"] == pytest.approx(1)
    prepared = Statevector.from_instruction(build_bv("110", stage="prepare"))
    assert prepared.probabilities_dict(qargs=[0, 1, 2])["000"] == pytest.approx(1/8)


def test_examples_do_not_share_state():
    assert [recover(alpha) for alpha in ["110", "010", "001", "1011", "110"]] == [
        "110", "010", "001", "1011", "110"
    ]


@pytest.mark.parametrize("alpha", ["", "012", "abc", " 01", None, 101, [0, 1]])
def test_invalid_secret_rejected(alpha):
    with pytest.raises(ValueError, match="nonempty binary string"):
        build_bv(alpha)


def test_invalid_stage_rejected():
    with pytest.raises(ValueError, match="stage"):
        build_bv("01", stage="unknown")
    with pytest.raises(ValueError, match="measurement"):
        build_bv("01", measure=True, stage="oracle")
