# Bernstein–Vazirani Algorithm with Qiskit

This project implements and explains the **Bernstein–Vazirani quantum algorithm** using Qiskit.

The algorithm determines a hidden bit string encoded inside a black-box function. A classical deterministic approach may require multiple queries, while the quantum algorithm can recover the entire bit string with a single oracle query.

## Project Overview

The notebook walks through:

- the Bernstein–Vazirani problem
- quantum-circuit construction
- oracle implementation
- Hadamard transformations
- circuit simulation
- measurement results
- recovery of the hidden bit string

## Repository Contents

- `bernstein_vazirani.ipynb`  
  Main implementation and explanation of the Bernstein–Vazirani algorithm.

## How It Works

Suppose a hidden bit string is:

```text
s = 1011
```

The oracle represents the function:

```text
f(x) = s · x mod 2
```

The Bernstein–Vazirani algorithm uses quantum superposition and interference to recover the hidden string after a single oracle query.

The circuit:

1. prepares the input qubits in superposition
2. applies the Bernstein–Vazirani oracle
3. applies Hadamard gates again
4. measures the input register
5. recovers the hidden bit string from the measurement result

## Tech Stack

- Python
- Qiskit
- Qiskit Aer
- Jupyter Notebook

## Running the Project

Install the required packages:

```bash
pip install qiskit qiskit-aer
```

Then open:

```text
bernstein_vazirani.ipynb
```

in Jupyter Notebook, JupyterLab, or Google Colab.

## What I Learned

This project helped me understand how quantum algorithms use superposition, interference, and oracle-based computation to extract information more efficiently than a straightforward classical query process.

It also gave me experience constructing and simulating quantum circuits with Qiskit.
