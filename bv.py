"""Ideal Bernstein–Vazirani circuits with an explicit displayed-bit convention.

``alpha`` is written q_(n-1)...q_0: its rightmost bit maps to qubit zero.
The ancilla is qubit n. Statevector probabilities marginalize over that ancilla.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

STAGES = ("initialize", "prepare", "oracle", "final")


def build_bv(alpha: str, measure: bool = False, *, stage: str = "final") -> QuantumCircuit:
    """Build a full circuit or a teaching snapshot from the same implementation.

    ``initialize`` flips the ancilla; ``prepare`` adds initial Hadamards;
    ``oracle`` additionally applies the parity oracle; ``final`` decodes inputs.
    Measurement is available only for the final stage.
    """
    if not isinstance(alpha, str) or not alpha or set(alpha) - {"0", "1"}:
        raise ValueError("alpha must be a nonempty binary string")
    if stage not in STAGES:
        raise ValueError(f"stage must be one of {STAGES}")
    if measure and stage != "final":
        raise ValueError("measurement is supported only for the final stage")
    n = len(alpha)
    circuit = QuantumCircuit(n + 1, n) if measure else QuantumCircuit(n + 1)
    circuit.x(n)
    if stage == "initialize":
        return circuit
    circuit.h(range(n + 1))
    if stage == "prepare":
        return circuit
    for qubit, bit in enumerate(reversed(alpha)):
        if bit == "1":
            circuit.cx(qubit, n)
    if stage == "oracle":
        return circuit
    circuit.h(range(n))
    if measure:
        circuit.measure(range(n), range(n))
    return circuit


def input_probabilities(alpha: str) -> dict[str, float]:
    """Return the complete ideal input-register distribution, without thresholding."""
    state = Statevector.from_instruction(build_bv(alpha))
    return {
        str(key): float(value)
        for key, value in state.probabilities_dict(qargs=list(range(len(alpha)))).items()
    }


def recover(alpha: str) -> str:
    """Return the most likely ideal outcome; this is not a hardware measurement."""
    probabilities = input_probabilities(alpha)
    return max(probabilities, key=probabilities.get)
