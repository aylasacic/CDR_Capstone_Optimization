import argparse
import numpy as np
import random
from math import pi
from mitigation import (
    RotationTransformer,
    generate_original_circuit,
    simulate_noisy_expectation,
    simulate_exact_expectation,
    perform_regression,
    plot_regression,
    mitigate_expectation
)
from qiskit import transpile
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.quantum_info import Pauli, Statevector
import matplotlib.pyplot as plt

def train(args):
    """
        train the regression model for CDR

        does not return anything, but saved model to local file
    """

    # set number of qubits
    nqubits = 2
    # set number of shots for measurements of quantum circuits
    nshots = 4096
    # set the number of training circuits
    num_training = 1000
    # limit to difference between noisy and real values acceptable to append to out values
    # without this, some values are quite random in the noisy values and LR would not work as well
    parity_threshold = 0.05

    # generate the original circuit
    qc = generate_original_circuit(nqubits)

    # apply the RotationTransformer to generate training circuits
    transformer = RotationTransformer(N = 0.3)
    # intialize list of circuits without measurement
    training_circuits_no_measurement_all = []  
    for _ in range(num_training):
        training_circuits_no_measurement_all.append(RotationTransformer()(qc))

    # calculate exact expectation value
    exp_val_qc = simulate_exact_expectation(qc, observable = 'ZZ')
    print('Exact expectation value of the original circuit:', exp_val_qc)

    # filter training circuits based on expectation value proximity
    noiseless_exp_vals = []
    # list for the values which fall within the parity_threshold
    training_circuits_no_measurement = []
    observable = 'ZZ'
    for circuit in training_circuits_no_measurement_all:
        # get expectation value
        expectation_value = simulate_exact_expectation(circuit, observable = observable)
        # if expectation_value is within the parity_threshold limit
        if (exp_val_qc - parity_threshold) <= expectation_value <= (exp_val_qc + parity_threshold):
            # append it to the list
            noiseless_exp_vals.append(expectation_value)
            training_circuits_no_measurement.append(circuit)

    # print how many successfull circuits were made
    print(f'Number of training circuits within ±{parity_threshold} of the exact expectation value:', len(noiseless_exp_vals))

    # prepare training circuits with measurement
    training_circuits_with_measurement = []
    for circuit in training_circuits_no_measurement:
        # initialize quantum and classical registers
        qr = QuantumRegister(nqubits)
        cr = ClassicalRegister(nqubits)
        # initialize quantum circuit
        circ = QuantumCircuit(qr, cr)
        # convert the entire QuantumCircuit into a single Instruction object.
        circ.append(circuit.to_instruction(), qr)
        # measure circuit
        circ.measure(qr, cr)
        # append the cirucit to measurement list
        training_circuits_with_measurement.append(circ)

    # simulate noisy expectation values
    noisy_exp_vals = simulate_noisy_expectation(training_circuits_with_measurement, nshots = nshots)

    # remove any None values that might have been appended
    valid_indices = [i for i, val in enumerate(noisy_exp_vals) if val is not None]
    noisy_exp_vals_filtered = [noisy_exp_vals[i] for i in valid_indices]
    noiseless_exp_vals_filtered = [noiseless_exp_vals[i] for i in valid_indices]

    # perform regression for given data
    model = perform_regression(noisy_exp_vals_filtered, noiseless_exp_vals_filtered)
    print(f"Regression model: y = {model.coef_[0]:.4f} * x + {model.intercept_:.4f}")

    # plot regression
    plot_regression(noisy_exp_vals_filtered, noiseless_exp_vals_filtered, model)

    # save the model parameters for later use
    np.savez('regression_model.npz', slope=model.coef_[0], intercept=model.intercept_)
    print("Training completed and model saved as 'regression_model.npz'.")

def predict(args):
    """
        predict value of a quantum circuit generated

        does not return anything, but saved model to local file
    """
    # set number of qubits
    nqubits = 2
    # set number of shots
    nshots = 4096
    # set the Pauli observable
    observable = 'ZZ'

    # load the regression model parameters
    try:
        data = np.load('regression_model.npz')
        slope = data['slope']
        intercept = data['intercept']
    except FileNotFoundError:
        print("Regression model not found. Please run the training first.")
        return

    # generate the original circuit
    qc = generate_original_circuit(nqubits)
    print(qc)

    # prepare the circuit with measurement (same as in training)
    qr_qc = QuantumRegister(nqubits)
    cr_qc = ClassicalRegister(nqubits)
    circ_qc = QuantumCircuit(qr_qc, cr_qc)
    circ_qc.append(qc.to_instruction(), [qubit for qubit in range(nqubits)])
    circ_qc.measure(qr_qc, cr_qc)

    # simulate noisy expectation value
    noisy_exp_val = simulate_noisy_expectation([circ_qc], nshots=nshots)[0]
    if noisy_exp_val is None:
        print("Noisy expectation value could not be determined.")
        return

    # print the unmitigated expectation value
    print('Unmitigated expectation value:', noisy_exp_val)

    # apply mitigation
    mitigated_exp_val = slope * noisy_exp_val + intercept
    print('Mitigated expectation value:', mitigated_exp_val)

    # calculate exact expectation value
    exp_val_qc = simulate_exact_expectation(qc, observable=observable)
    print('Exact expectation value:', exp_val_qc)

    # error calculation
    error_unmitigated = abs(noisy_exp_val - exp_val_qc)
    error_mitigated = abs(mitigated_exp_val - exp_val_qc)
    print("Error (unmitigated):", error_unmitigated)
    print("Error (mitigated):", error_mitigated)

    if exp_val_qc != 0:
        print("Relative error (unmitigated):", error_unmitigated / abs(exp_val_qc))
        print("Relative error (mitigated):", error_mitigated / abs(exp_val_qc))
    else:
        print("Exact expectation value is zero; relative error is undefined.")

    if error_unmitigated != 0:
        print(f"Error reduction with mitigation: {(error_unmitigated - error_mitigated) / error_unmitigated:.1%}.")
    else:
        print("Unmitigated error is zero; no reduction possible.")

def main():
    # get comand line arguments and print necessary help instructions
    # see argparser documentation for help
    parser = argparse.ArgumentParser(description = 'Quantum Error Mitigation CLI')
    subparsers = parser.add_subparsers(dest = 'command', required=True)

    # Train command
    train_parser = subparsers.add_parser('train', help = 'Train the error mitigation model')

    # Predict command
    pred_parser = subparsers.add_parser('pred', help = 'Predict using the trained error mitigation model')

    args = parser.parse_args()

    if args.command == 'train':
        train(args)
    elif args.command == 'pred':
        predict(args)

# run main
if __name__ == '__main__':
    main()
