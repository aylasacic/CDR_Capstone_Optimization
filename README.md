# CDR Sandbox Testing Tool

Quantum error mitigation (EM) is an essential practice in the current Noisy Intermediate-Scale Quantum (NISQ) of quantum computing. It provides a reliable baseline for the reduction of the severity of mistakes on quantum devices and holds an important role in near term quantum computing, especially with hybrid quantum algorithms. It is hence of great importance to establish proper groundwork that would enable a clear understanding of how EM can be improved upon, especially when it involves machine learning principles. The technique known as Clifford Data Regression (CDR) is one of the most known mitigation techniques which involves training a model on noisy and exact quantum data and promoting it to infer results from that data on a circuit of interest. This study investigates the optimization of CDR through the incorporation of regularization methods, specifically Lasso and Ridge regression, to improve its effectiveness and robustness. We implemented the optimized CDR framework on quantum circuits comprising 2, 4, and 6 qubits, utilizing a simulated noisy backend to evaluate performance. Our results demonstrate that regularized regression models substantially reduce computational errors, achieving up to a 91.7\% average improvement in error reduction for 2-qubit systems using Lasso regression. For 4 and 6-qubit systems, Lasso and Ridge regression maintained better performance compared to standard linear regression, though the degree of improvement diminished with increasing qubit counts. Additionally, regularization mitigated the risk of overfitting, particularly in scenarios where noisy expectation values closely approached their exact values. These results show that combining classical machine learning techniques with quantum error mitigation can improve the accuracy of quantum computations on NISQ devices. In the future, we aim to tackle scalability issues and further refine our regression models to ensure they perform well with larger and more complex quantum systems.

Part II: Second part of the capstone which implement a simple H2 VQE from: and applied the optimized CDR. It also implements ensamble techniques such as Random Forest and XGBoost models while keeping the regularization techniques. It shows that the regularization techniques outpreform the ensamble techniques for the simple H2 case VQE.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Install the Package](#4-install-the-package)
- [Usage](#usage)
  - [Training the Model](#training-the-model)
  - [Prediction (Mitigation)](#prediction-mitigation)
- [Project Structure](#project-structure)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Circuit Transformation**: Replace non-Clifford gates with Clifford-equivalent gates based on a specified probability.
- **Training Phase**: Generate and simulate training circuits to build a regression model that maps noisy expectation values to noiseless ones.
- **Prediction Phase**: Apply the trained regression model to mitigate errors in new quantum circuits (the circuits are of the same structure as ones trained on).
- **Command-Line Interface (CLI)**: Easy-to-use CLI with `train` and `pred` commands.

## Prerequisites

Before setting up the tool, ensure you have the following installed on your system:

- **Python 3.7 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python's package installer. 
  
  ```bash
  pip --version
  ```

## Installation

Follow the steps below to set up the CDR on your machine.

### 1. Clone the Repository

First, clone the repository to your local machine. Replace `<repository_url>` with the actual URL of your repository.

```bash
git clone <repository_url>
cd repository_name
```

*If you don't have a repository and are setting this up locally, you can skip the cloning step and proceed to create the project directory.*

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies without affecting your global Python installation.

**Using `venv`:**

```bash
python -m venv quantum_env
```

**Activate the Virtual Environment:**

- **Windows:**

  ```bash
  quantum_env\Scripts\activate
  ```

- **macOS/Linux:**

  ```bash
  source quantum_env/bin/activate
  ```

*Your terminal prompt should now indicate that the virtual environment is active.*

### 3. Install Dependencies

Install the required Python packages using `pip`. Ensure you're in the root directory of the project where the `requirements.txt` file is located.

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```plaintext
qiskit
qiskit-aer
numpy
scikit-learn
matplotlib
joblib
tqdm
```

*If any dependencies are missing, add them to the `requirements.txt` file and rerun the installation command.*

### 4. Install the Package

Install the CDR Sandbox package in editable mode. 

```bash
pip install -e .
```

*The `-e` flag stands for "editable" mode.*

### 5. Verify Installation

Ensure that the CLI is correctly installed by checking the help message.

```bash
cdr_sandbox --help
```

**Expected Output:**

```plaintext
CDR Sandbox CLI

positional arguments:
  {train,pred}
    train       Train the error mitigation model
    pred        Predict using the trained error mitigation model

optional arguments:
  -h, --help    show this help message and exit
```

---

## Usage

The tool provides a Command-Line Interface (CLI) with two primary commands:

- `train`: Train the error mitigation model.
- `pred`: Apply the trained model to mitigate errors in a quantum circuit.

### Training the Model

The training process involves generating transformed circuits, simulating them in a noisy environment, and performing regression to map noisy expectation values to noiseless ones.

**Command:**

```bash
cdr_sandbox train
```

**Optional Arguments (NOT YET IMPLEMENTED):**

- `--nqubits`: Number of qubits (default: 2)
- `--nshots`: Number of shots/simulations (default: 20000)
- `--num_training`: Number of training circuits to generate (default: 10000)
- `--parity_threshold`: Threshold for selecting training circuits based on expectation value proximity (default: 0.05)
- `--transformation_prob`: Probability of transforming non-Clifford gates (default: 0.3)

**Example with Custom Parameters:**

```bash
cdr_sandbox train (--nqubits 3 --nshots 30000 --num_training 15000 --parity_threshold 0.1 --transformation_prob 0.4 -> not yet implemented)
```

**Expected Output:**

1. **Progress Indicators:**

   ```
   Processed 1000/10000 circuits
   Processed 2000/10000 circuits
   ...
   Processed 10000/10000 circuits
   ```

2. **Exact Expectation Value:**

   ```
   Exact expectation value of the original circuit: 0.6543
   ```

3. **Number of Training Circuits Within Threshold:**

   ```
   Number of training circuits within ±0.05 of the exact expectation value: 500
   ```

4. **Simulation and Regression Details:**

   ```
   Simulating noisy expectation values...
   Number of valid training samples after filtering: 500
   Regression model: y = 0.85 * x + 0.02
   Training completed and model saved as 'regression_model.joblib'.
   ```

5. **Regression Plot:**

   - A plot named `regression_plot.png` saved in the project directory visualizing the regression fit.

### Prediction (Mitigation)

Apply the trained regression model to mitigate errors in a new quantum circuit.

**Command:**

```bash
cdr_sandbox pred
```

**Optional Arguments (NOT YET IMPLEMENTED):**

- `--nqubits`: Number of qubits (default: 2)
- `--nshots`: Number of shots/simulations (default: 20000)
- `--observable`: Observable to measure (default: 'ZZ')

**Example with Custom Parameters:**

```bash
cdr_sandbox pred (--nqubits 3 --nshots 4096 --observable 'XX' -> yet to be implemented)
```

**Expected Output:**

1. **Loaded Regression Model:**

   ```
   Loaded regression model: y = 0.85 * x + 0.02
   ```

2. **Simulation Details:**

   ```
   Simulating noisy expectation value for the original circuit...
   ```

3. **Expectation Values and Error Calculations:**

   ```
   Unmitigated expectation value: -0.1234
   Mitigated expectation value: 0.0593
   Exact expectation value: 0.6543
   Error (unmitigated): 0.7777
   Error (mitigated): 0.5950
   Relative error (unmitigated): 1.1855
   Relative error (mitigated): 0.9081
   Error reduction with mitigation: 23.2%.
   ```

*Ensure that you have successfully run the `train` command before executing `pred`.*

---

## Project Structure

Here's an overview of the project's directory structure:

```
CDR_Optimization_as15471/
├── mitigation/
│   ├── __init__.py
│   ├── transformer.py
│   ├── circuit_generator.py
│   ├── simulation.py
│   ├── regression.py
│   └── mitigation.py
├── scripts/
│   └── cli.py
├── requirements.txt
├── setup.py
└── README.md
```

- **cdr_sandbox/**: Python package containing all modules.
  - **transformer.py**: Contains the `RotationTransformer` class for circuit transformations.
  - **circuit_generator.py**: Functions to generate and append gates to quantum circuits.
  - **simulation.py**: Functions for simulating quantum circuits and calculating expectation values.
  - **regression.py**: Functions for performing and handling regression models.
  - **mitigation.py**: Functions to apply mitigation to expectation values.
- **scripts/**: Contains the CLI script.
  - **cli.py**: Implements the command-line interface with `train` and `pred` commands.
- **requirements.txt**: Lists all Python dependencies.
- **setup.py**: Facilitates package installation.
- **README.md**: Project documentation (this file).

---



## Acknowledgements

- [Piotr Czarnik et al.](https://arxiv.org/search/quant-ph?searchtype=author&query=Czarnik,+P) for their research in CDR and his [original CDR paper ](https://arxiv.org/abs/2005.10189) where most of the implementation came from.
- [Renata Wong](https://github.com/renatawong) for their [CDR implementation](https://github.com/renatawong/clifford-data-regression-qiskit) on GitHub which served as big inspiration in the code written in this project.s

---

## Contact

For any questions or suggestions, feel free to contact [Ajla Šačić](mailto:as15471@nyu.com).

---

**Happy Quantum Computing!**
