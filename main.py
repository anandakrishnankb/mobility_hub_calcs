import numpy as np
from fractions import Fraction

def parse_value(value_str):
    try:
        # Try to convert the value to an integer
        return int(value_str)
    except ValueError:
        try:
            # Try to parse the value as a fraction
            return float(Fraction(value_str))
        except ValueError:
            # If parsing fails, return 0
            return 0.0

def get_PR_values():
    n = int(input("Enter the number of PRs: "))
    PR_values = {}
    for i in range(1, n+1):
        PR = input(f"Enter the value for PR{i}: ")
        num_sub_PRs = int(input(f"Enter the number of sub PRs for PR{i}: "))
        sub_PRs = {}
        for j in range(1, num_sub_PRs+1):
            sub_PR = input(f"Enter the value for sub PR{i}{j}: ")
            sub_PRs[f"PR{i}{j}"] = sub_PR
        PR_values[f"PR{i}"] = {"value": PR, "sub_PRs": sub_PRs}
    return PR_values
def get_matrix_values(PR_values):
    n = len(PR_values)
    matrix = []
    print("Enter the values for the matrix:")
    print("Leave blank for diagonal elements (PRi == PRj).")
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                value = 1.0  # Diagonal elements are always 1
            else:
                value_str = input(f"Enter the value for cell (PR{i+1}, PR{j+1}): ")
                if value_str.strip():  # Check if the input is not empty
                    value = float(Fraction(value_str))
                else:
                    value = 0.0  # If empty, consider it as 0
            row.append(value)
        matrix.append(row)
    return matrix

def print_matrix(matrix, PR_values):
    n = len(matrix)
    print("Matrix:")
    # Print column headers
    print("   ", end="")
    for i in range(1, n + 1):
        print(f"PR{i:<4}", end="")
    print()
    # Print matrix with row headers
    for i in range(n):
        print(f"PR{i+1:<3}", end="")
        for j in range(n):
            print(str(matrix[i][j]).ljust(4), end="")
        print()

def calculate_CR(pairwise_matrix):
    n = len(pairwise_matrix)

    # Step 1: Calculate normalized matrix
    column_sums = np.sum(pairwise_matrix, axis=0)
    normalized_matrix = pairwise_matrix / column_sums

    # Step 2: Calculate principal eigenvalue (λmax)
    eigenvalues, _ = np.linalg.eig(normalized_matrix)
    λmax = np.max(eigenvalues.real)

    # Step 3: Calculate Consistency Index (CI)
    CI = (λmax - n) / (n - 1)

    # Step 4: Random Index (RI) - computed dynamically
    RI_values = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    RI = RI_values.get(n)

    # Calculate the Random Index (RI) dynamically
    if n <= 9:
        RI = RI_values[n]
    else:
        # For n > 9, approximate RI using the formula RI ≈ 0.1 * n
        RI = 0.1 * n

    # Step 5: Calculate Consistency Ratio (CR)
    CR = CI / RI

    return CR





# Example usage:
# PR_values = get_PR_values()
# print(PR_values)
# matrix = get_matrix_values(PR_values)
# print_matrix(matrix, PR_values)
# CR = calculate_CR(np.array(matrix))
# print("Consistency Ratio (CR):", CR)

pairwise_matrix = [
    [1, 3, 3, 5, 5],
    [1/3, 1, 3, 5, 5],
    [1/3, 1/3, 1, 3, 3],
    [1/5, 1/5, 1/3, 1, 3],
    [1/5, 1/5, 1/3, 1/3, 1]
]

# Calculate CR using the provided function
CR = calculate_CR(pairwise_matrix)
print(CR)