# quantum_mitigation/circuit_generator.py

from qiskit import QuantumCircuit
from math import pi

def append_gates(qc, nqubits = 2):
    """
        append gates manually to a provided quantum circuit

        parameters:
        - qc (QuantumObject): initialized quantum cicuits to appends gates tp
        - nqubits (int): the number of qubits

        returns:
        - QuantumObject: the quantum circuit with appended gates
    """
    # for a specified depth
    for rep in range(7):
        for qubit in range(nqubits):
            qc.h(qubit)  
        for qubit in range(nqubits)[::2]:
            qc.rz(1.25, qubit)
        for qubit in range(nqubits)[1::2]:
            qc.rz(1.31, qubit)
        for qubit in range(nqubits)[::2]:
            qc.cx(qubit, qubit+1)     
        for qubit in range(nqubits)[::2]:
            qc.rx(-2.17, qubit)
        for qubit in range(nqubits)[1::2]:
            qc.ry(2.24, qubit)
        for qubit in range(nqubits):
            qc.rx(pi/2, qubit)    
    return qc

def generate_original_circuit(nqubits = 2):
    """
        generate the quantum circuit

        parameters:
        - nqubits (int): the number of qubits

        returns:
        - QuantumObject: the quantum circuit with appended gates
    """
    qc = QuantumCircuit(nqubits)
    append_gates(qc, nqubits)
    return qc
