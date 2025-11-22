# quantum_mitigation/transformer.py

from qiskit.converters import circuit_to_dag
from qiskit.transpiler import TransformationPass
from qiskit.circuit.library import RZGate, RXGate, RYGate
import numpy as np
import random
from math import pi, isclose
from qiskit import QuantumCircuit

class RotationTransformer(TransformationPass):
    """
        a transpiler pass that replaces RZ(a), RX(a), and RY(a) gates with their Clifford equivalents:
        - RZ(pi/2 * n)
        - RX(pi/2 * n) expressed as H RZ(pi/2 * n) H
        - RY(pi/2 * n) expressed as S H RZ(pi/2 * n) H S†
            where n = 0, 1, 2, 3, selected randomly based on a probability N.

        this pass transforms non-Clifford rotation gates into Clifford-equivalent gates with angles 
        of {0, pi/2, pi, 3*pi/2}, preserving the structure of the circuit.

        attributes:
        - N (float): the probability of replacing a non-Clifford rotation gate with a Clifford rotation gate.
        - clifford_angles (list): the list of Clifford angles to replace non-Clifford angles.
    """
    
    def __init__(self, N=0.3):
        """
            initialize the RotationTransformer pass with a given probability N.

            parameters:
            - N (float): the default value is 0.3, meaning there's a 30% chance of transformation.
        """
        super().__init__()
        self.N = N
        self.clifford_exponents = np.array([0.0, 0.5, 1.0, 1.5])
        self.clifford_angles = [exponent * np.pi for exponent in self.clifford_exponents]
        self.clifford_angles = [0, pi/2, pi, 3*pi/2]

    def run(self, dag):
        """
            apply the RotationTransformer pass on the directed acyclic graph (DAG) of a quantum circuit.
    
            the method iterates over all RZ, RX, and RY gates in the circuit, checks if the gate has a 
            non-Clifford angle (i.e., not a multiple of pi/2 within a tolerance), and probabilistically replaces it 
            with a Clifford rotation gate.
    
            parameters:
            - dag (DAGCircuit): the DAG representation of the quantum circuit to transform.
    
            returns:
            - DAGCircuit: the transformed DAG where applicable rotation gates are replaced with Clifford rotation gates.
        """
        # define the gates to transform
        rotation_gates = {
            RZGate: 'rz',
            RXGate: 'rx',
            RYGate: 'ry'
        }

        for gate_cls, gate_name in rotation_gates.items():
            # iterate over all instances of the current gate type in the DAG
            for node in list(dag.op_nodes(gate_cls)):  # Convert to list to avoid modification issues
                # get the angle of the gate
                angle = float(node.op.params[0])

                # normalize the angle to the range [0, 2*pi)
                normalized_angle = angle % (2 * pi)

                # check if the angle is a multiple of pi/2 within a tolerance
                is_clifford = any(
                    isclose(normalized_angle, cliff_angle, abs_tol = 1e-3) 
                    for cliff_angle in self.clifford_angles
                )

                if not is_clifford:
                    # decide whether to replace based on probability N
                    if random.random() < self.N:
                        # select a random Clifford angle
                        replacement_angle = random.choice(self.clifford_angles)

                        if gate_cls == RZGate:
                            # replace RZ with RZ(pi/2 * n)
                            replacement_circuit = QuantumCircuit(1, name = 'RZ_replacement')
                            replacement_circuit.rz(replacement_angle, 0)
                            dag.substitute_node_with_dag(node, circuit_to_dag(replacement_circuit))


                        elif gate_cls == RXGate:
                            # replace RX(pi/2 * n) with H RZ(pi/2 * n) H
                            replacement_circuit = QuantumCircuit(1, name='RX_replacement')
                            replacement_circuit.h(0)
                            replacement_circuit.rz(replacement_angle, 0)
                            replacement_circuit.h(0)
                            replacement_dag = circuit_to_dag(replacement_circuit)
                            dag.substitute_node_with_dag(node, replacement_dag)

                        elif gate_cls == RYGate:
                            # replace RY(pi/2 * n) with S H RZ(pi/2 * n) H S†
                            replacement_circuit = QuantumCircuit(1, name='RY_replacement')
                            replacement_circuit.s(0)
                            replacement_circuit.h(0)
                            replacement_circuit.rz(replacement_angle, 0)
                            replacement_circuit.h(0)
                            replacement_circuit.sdg(0)
                            replacement_dag = circuit_to_dag(replacement_circuit)
                            dag.substitute_node_with_dag(node, replacement_dag)

        return dag
