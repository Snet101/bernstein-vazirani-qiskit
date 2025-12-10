# Superposition
Notice: One of the files are pre run so it is pdf format from Jupyter Notebook, but the google collab is the interactive version.


Bernstein Vazirani Algorithm with Qiskit

This repository contains a Jupyter Notebook that demonstrates the **Bernstein-Vazirani quantum algorithm**, implemented using [Qiskit](https://qiskit.org/). The algorithm is designed to find a hidden bit string in a black-box function with **only one quantum query**, showcasing the power of quantum parallelism.

---

About the Algorithm

The **Bernstein–Vazirani algorithm** solves the problem of determining a hidden bitstring `s` given a function `f(x) = s · x mod 2`. While a classical algorithm would require `n` queries for an `n`-bit string, the quantum version solves it with a **single query** using quantum superposition and interference.

---

Contents

- `Bernstein_Vazirani (2).ipynb`: The main Jupyter notebook with:
  - Background explanation of the algorithm
  - Implementation in Qiskit
  - Visualization of quantum circuits
  - Simulation results using Qiskit Aer
  - Measurement analysis to extract the hidden bitstring

---

_Requirements_

Nothing, Everything is pre run and in pdf/google collab format
