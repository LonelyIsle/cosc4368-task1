# COSC 4368 AI Assignment - Task 1: Randomized Hill Climbing (RHCR2)

## Course Information
**Course:** COSC 4368 - Artificial Intelligence  
**Assignment:** Task 1 - Randomized Hill Climbing (RHCR2)

## Description
This project implements a Python script for Task 1 of the COSC 4368 AI assignment. The script demonstrates the Randomized Hill Climbing algorithm, specifically the RHCR2 variant, for solving a combinatorial optimization problem. A new command-line option `--seed` has been added to allow easy specification of the random seed at runtime, helping graders reproduce runs consistently.

## How to Run
Make sure you are in the directory containing `task1.py`.  
To execute the script, run:
```
python task1.py
```
To override the random seed used for the runs, use the `--seed` option:
```
python task1.py --seed 12345
```

## Output Explanation
After running, the script will output a table with results for each experiment. The columns are:
- **Sol1 / Sol2 / Sol3**: The solution vectors found by the algorithm in each of three independent runs.
- **f(Sol1) / f(Sol2) / f(Sol3)**: The objective function value for each solution.
- **N1 / N2 / N3**: The number of function evaluations (or steps) used in each run.
- **Total Calls**: The total number of function calls across all runs.
- **Seed**: The random seed used for reproducibility.

You can copy-paste the table output directly into Google Docs or Google Sheets for inclusion in your assignment report.

## Dependencies
- Requires **Python 3**.
- No external packages are needed; the script uses only standard Python libraries.

## Customizing Parameters
You can adjust the following parameters by editing the top of `task1.py`:
- `sp`: Starting point or initial solution.
- `p`: Probability parameter for the algorithm.
- `z`: Number of iterations or another algorithm-specific parameter.
- `seed`: Random seed for reproducibility.

Alternatively, you can now pass the seed at runtime using the `--seed` command-line flag. The script uses this base seed and applies an internal formula to generate different seeds for each run, ensuring reproducibility and variation across runs. This feature facilitates graders in reproducing and verifying the results easily.