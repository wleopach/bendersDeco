# Traveling Salesman Problem (TSP) Solver

This repository contains a solver for the Traveling Salesman Problem (TSP) using Gurobi.
The implementation demonstrates the use of callback functions to add lazy constraints for subtour elimination, 
ensuring that the solution forms a single tour that visits each city exactly once.

In particular the idea of this project is to explore the relationship of
the presented solution with Benders Decomposition.

## Features

- Calculates Euclidean distances between cities.
- Implements the subtour elimination method using lazy constraints.
- Utilizes Gurobi's powerful optimization capabilities.
- Illustrates the use of Benders decomposition for solving TSP.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/tsp-solver.git
    cd tsp-solver
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the TSP solver:
```sh
python example.py
