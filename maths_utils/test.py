import re
from collections import defaultdict

def parse_equation(eq):
    """Parse a linear equation and return coefficients and RHS value."""
    eq = eq.replace(" ", "")
    
    # Handle different equation formats
    if '=' not in eq:
        raise ValueError("Equation must contain '=' sign")
    
    lhs, rhs = eq.split('=')
    
    # Parse RHS (right-hand side)
    rhs_coeffs = defaultdict(float)
    rhs_const = 0.0
    
    # Find variable terms on RHS
    rhs_var_terms = re.findall(r'([+-]?\d*\.?\d*)([a-zA-Z]+)', rhs)
    for coeff, var in rhs_var_terms:
        if coeff in ('', '+'):
            coeff = 1.0
        elif coeff == '-':
            coeff = -1.0
        else:
            coeff = float(coeff)
        rhs_coeffs[var] += coeff
    
    # Find constant terms on RHS
    rhs_const_terms = re.findall(r'([+-]?\d+\.?\d*)(?![a-zA-Z])', rhs)
    for const in rhs_const_terms:
        rhs_const += float(const)
    
    # Parse LHS (left-hand side)
    lhs_coeffs = defaultdict(float)
    lhs_const = 0.0
    
    # Find variable terms on LHS
    lhs_var_terms = re.findall(r'([+-]?\d*\.?\d*)([a-zA-Z]+)', lhs)
    for coeff, var in lhs_var_terms:
        if coeff in ('', '+'):
            coeff = 1.0
        elif coeff == '-':
            coeff = -1.0
        else:
            coeff = float(coeff)
        lhs_coeffs[var] += coeff
    
    # Find constant terms on LHS
    lhs_const_terms = re.findall(r'([+-]?\d+\.?\d*)(?![a-zA-Z])', lhs)
    for const in lhs_const_terms:
        lhs_const += float(const)
    
    # Move everything to LHS (standard form: ax + by + c = 0)
    final_coeffs = defaultdict(float)
    for var in set(list(lhs_coeffs.keys()) + list(rhs_coeffs.keys())):
        final_coeffs[var] = lhs_coeffs[var] - rhs_coeffs[var]
    
    final_rhs = rhs_const - lhs_const
    
    return final_coeffs, final_rhs

def build_matrix(equations):
    """Build coefficient matrix and RHS vector from equations."""
    variables = set()
    parsed = []
    
    for eq in equations:
        coeffs, rhs = parse_equation(eq)
        parsed.append((coeffs, rhs))
        variables.update(coeffs.keys())
    
    variables = sorted(list(variables))
    
    A = []
    b = []
    
    for coeffs, rhs in parsed:
        row = [coeffs.get(var, 0.0) for var in variables]
        A.append(row)
        b.append(rhs)
    
    return A, b, variables

def solve_linear_system(A, b):
    """Solve linear system using Gaussian elimination."""
    n = len(A)
    m = len(A[0]) if n > 0 else 0
    
    # Check for valid system
    if n == 0 or m == 0:
        return "Empty system"
    
    # Create augmented matrix
    aug_matrix = []
    for i in range(n):
        aug_matrix.append(A[i][:] + [b[i]])
    
    # Forward elimination with partial pivoting
    for i in range(min(n, m)):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(aug_matrix[j][i]) > abs(aug_matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        aug_matrix[i], aug_matrix[max_row] = aug_matrix[max_row], aug_matrix[i]
        
        # Check for zero pivot
        if abs(aug_matrix[i][i]) < 1e-12:
            continue
        
        # Eliminate column
        for j in range(i + 1, n):
            if abs(aug_matrix[j][i]) > 1e-12:
                ratio = aug_matrix[j][i] / aug_matrix[i][i]
                for k in range(i, m + 1):
                    aug_matrix[j][k] -= ratio * aug_matrix[i][k]
    
    # Check for inconsistency
    for i in range(n):
        all_zero = True
        for j in range(m):
            if abs(aug_matrix[i][j]) > 1e-12:
                all_zero = False
                break
        if all_zero and abs(aug_matrix[i][m]) > 1e-12:
            return "No solution (inconsistent system)"
    
    # Back substitution
    if n != m:
        return "System is underdetermined or overdetermined"
    
    x = [0] * n
    for i in reversed(range(n)):
        if abs(aug_matrix[i][i]) < 1e-12:
            return "No unique solution"
        
        x[i] = aug_matrix[i][m]
        for j in range(i + 1, n):
            x[i] -= aug_matrix[i][j] * x[j]
        x[i] /= aug_matrix[i][i]
    
    return x

def solve_equations(equations):
    """Solve a system of linear equations."""
    try:
        A, b, variables = build_matrix(equations)
        solution = solve_linear_system(A, b)
        
        if isinstance(solution, str):
            return solution
        
        return dict(zip(variables, solution))
    
    except Exception as e:
        return f"Error: {str(e)}"

# Test cases
if __name__ == "__main__":
    # Test the original example (fixed input format)
    print("Test 1:")
    print(solve_equations(["5z + 6y + 3 = 0", "6y + 5 = 0"]))
    
    # Test various forms of linear equations
    print("\nTest 2 - Standard form:")
    print(solve_equations(["2x + 3y = 7", "x - y = 1"]))
    
    print("\nTest 3 - Variables on both sides:")
    print(solve_equations(["2x + y = 3x + 5", "x + 2y = 7"]))
    
    print("\nTest 4 - Three variables:")
    print(solve_equations(["x + y + z = 6", "2x - y + z = 3", "x + 2y - z = 1"]))
    
    print("\nTest 5 - Negative coefficients:")
    print(solve_equations(["-2x + 3y = -1", "4x - 6y = 2"]))
    
    print("\nTest 6 - Decimal coefficients:")
    print(solve_equations(["1.5x + 2.5y = 4", "0.5x - 1.5y = -2"]))