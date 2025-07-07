import cmath
import re #import of regular Expression module parse input Expression

# Check in Front-end :
#     1.Equation should contain '='.
#     2.Equation should have a "x^2" term.

steps = ""

def extract_coefficients(equation):
    # Detect variable (e.g., x, y, z)
    match_var = re.search(r'([a-zA-Z])\^?2?', equation)
    if not match_var:
        raise ValueError("No variable found in the equation.")
    var = match_var.group(1)

    # Normalize terms: Add '+' at the beginning if missing
    if equation[0] not in "+-":
        equation = "+" + equation

    # Find all terms using regex
    terms = re.findall(rf'([+-]?\d*\.?\d*){var}\^2|([+-]?\d*\.?\d*){var}(?!\^)|([+-]?\d+\.?\d*)', equation)

    # Initialize coefficients
    a = b = c = 0.0

    # Sum up coefficients
    for quad, lin, const in terms:
        if quad:  # Quadratic term (a*var^2)
            coeff = quad if quad not in ('+', '-', '') else quad + '1' if quad in ('+', '-') else '1'
            a += float(coeff)
        elif lin:  # Linear term (b*var)
            coeff = lin if lin not in ('+', '-', '') else lin + '1' if lin in ('+', '-') else '1'
            b += float(coeff)
        elif const:  # Constant term (c)
            c += float(const)

    return a, b, c, var

def convert_to_default_format(equation):
    # Remove whitespace and '=0' if present
    equation = equation.replace(" ", "")
    equation = equation.replace("=0", "")
    
    # Split the equation into left and right parts
    if '=' in equation:
        left, right = equation.split('=')
    else:
        left, right = equation, '0'
    return left, right

def find_roots(a, b, c):
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero in a quadratic equation.")
    global steps
    discriminant = b**2 - 4*a*c
    steps += f"Using Sridharacharya's Formula: [(-b ± √(b² - 4ac)) / (2a)]\n"
    steps += f"In above equation: a = {a}, b = {b}, c = {c}\n"
    steps += f"Discriminant: ({b})² - 4*({a})*({c}) = {discriminant}\n"
    
    sqrt_disc = cmath.sqrt(discriminant)
    steps += f"Square root of Discriminant: ±√{discriminant} = {sqrt_disc}\n"
    
    root1 = (-b + sqrt_disc) / (2 * a)
    root2 = (-b - sqrt_disc) / (2 * a)
    steps += f"Root 1 and Root 2: ({-b} ± {sqrt_disc}) / (2*{a})\n"
    steps += f"Root 1: {root1}\nRoot 2: {root2}\n"
    
    vertex_x = -b / (2 * a)
    vertex_y = -discriminant / (4 * a)
    vertex = (vertex_x, vertex_y)
    steps += f"Vertex: ({-b}/(2*{a}), {-discriminant}/(4*{a})) = {vertex}\n"
    steps += f"Y-intercept of Equation: c = {c}\n"
    
    x_range = max(
        abs(root1 - vertex_x),
        abs(root2 - vertex_x),
        abs(0 - vertex_x)
    )

    # Generate x and y values for graphing
    x = [vertex_x + i * x_range / 100 for i in range(-150, 151)]
    y = [a * xi**2 + b * xi + c for xi in x]
    
    return root1, root2, vertex, x, y, c

def solution(equation):
    global steps
    steps = "" 
    try:
        left, right = convert_to_default_format(equation)
        a, b, c, var = extract_coefficients(left)
        if right != '0':
            d, e, f, _ = extract_coefficients(right)
            a -= d
            b -= e 
            c -= f
        steps += f"Input Equation : ({a}){var}^2+({b}){var}+({c})=0\n"
        return find_roots(a, b, c),var,steps,(a,b,c)
    except Exception as e:
        return f"Error: {str(e)}"
    
def solve_quadratic(equation):
    ((root1,root2,vertex,x,y,c),var,steps,(a,b,c)) = solution(equation)
    result = {
        "result" :f"Roots: {root1}, {root2}\n Vertex: {vertex}\n Y-Intercept: {c}",
        "steps": steps,
        "plot_info": {
            "root1": {"real": root1.real, "imag": root1.imag},
            "root2": {"real": root2.real, "imag": root2.imag},
            "variable": var,
            "vertex": vertex,
            "y_intercept": c,
            "abc":[a,b,c]
        },
        "plot_array" : {"x": x, "y": y,},
    }
    return result

