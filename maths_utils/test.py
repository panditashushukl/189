import re
from collections import defaultdict

def parse_equation(eq):
    # Remove all spaces
    eq = eq.replace(" ", "")
    # Split at '='
    lhs, rhs = eq.split('=')
    rhs = float(rhs)

    # Find all variable terms using regex
    # Matches like: '+3x', '-x', '4y', etc.
    terms = re.findall(r'([+-]?\d*\.?\d*)([a-zA-Z]+)', lhs)
    
    coeffs = defaultdict(float)
    for coeff, var in terms:
        if coeff in ('', '+'):
            coeff = 1.0
        elif coeff == '-':
            coeff = -1.0
        else:
            coeff = float(coeff)
        coeffs[var] += coeff  # combine like terms

    return coeffs, rhs

def build_matrix(equations):
    variables = set()
    parsed = []

    for eq in equations:
        coeffs, rhs = parse_equation(eq)
        parsed.append((coeffs, rhs))
        variables.update(coeffs.keys())

    variables = sorted(list(variables))  # consistent ordering

    A = []
    b = []
    for coeffs, rhs in parsed:
        row = [coeffs.get(var, 0.0) for var in variables]
        A.append(row)
        b.append(rhs)

    return A, b, variables

def solve_linear_system(A, b):
    n = len(A)
    # Append b to A to form augmented matrix
    for i in range(n):
        A[i].append(b[i])

    # Forward elimination
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]

        if abs(A[i][i]) < 1e-12:
            return "No unique solution."

        for j in range(i + 1, n):
            ratio = A[j][i] / A[i][i]
            for k in range(i, n + 1):
                A[j][k] -= ratio * A[i][k]

    # Back substitution
    x = [0] * n
    for i in reversed(range(n)):
        x[i] = A[i][n]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]

    return x

def solve_equations(equations):
    A, b, variables = build_matrix(equations)
    solution = solve_linear_system(A, b)
    if isinstance(solution, str):
        return solution
    return dict(zip(variables, solution))

print(solve_equations("5z+3=0"))