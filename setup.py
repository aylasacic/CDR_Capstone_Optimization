# setup.py

from setuptools import setup, find_packages

setup(
    name='cdr_sandbox',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'qiskit',
        'qiskit-aer',
        'numpy',
        'scikit-learn',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'cdr_sandbox= scripts.cli:main',
        ],
    },
    author='ajla',
    description='Quantum Error Mitigation using Clifford Data Regression',
)
