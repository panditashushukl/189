import cmath
import re #import of regular Expression module parse input Expression
import matplotlib.pyplot as plt
from io import BytesIO
import base64
#For third block
def find_quadratic_roots(equation):
    try:
        # Use regular expression to extract coefficients
        input_equation(equation)
        equation = re.sub(r'[a-z]', 'x', equation)
        a,b,c=get_abc(equation)
    except (ValueError, TypeError, ZeroDivisionError):
        return "Invalid input. Please provide a valid quadratic equation."

   
    root1,root2 = find_roots(a, b, c)
    return f"Root 1 : {root1}\nRoot 2 : {root2}\n"

def get_abc(equation) :
    match = re.search(r'([-+]?\d*)x\^2\s*([-+]?\d*)x\s*([-+]?\d*)=0', equation)  

    if match:
            a, b, c = extract_coefficients(equation)
    else:
            l,r=convert_to_default_format(equation)
            _,a,b,c= extract_coefficients_and_constants(l)
            _,d,e,f= extract_coefficients_and_constants(r)
            a=a-d
            b=b-e
            c=c-f
    return a,b,c



def input_equation(equation):
    return equation

def quadratic_steps(equation):
    steps = []
    try:

        equation = input_equation(equation)
        result = f"Input Equation : {equation}\n"
        match = re.search(r'([-+]?\d*)x\^2\s*([-+]?\d*)x\s*([-+]?\d*)=0', equation)  
        if match:
            a, b, c = extract_coefficients(equation)
        else:
            l,r=convert_to_default_format(equation)
            result1,a,b,c= extract_coefficients_and_constants(l)
            result2,d,e,f= extract_coefficients_and_constants(r)
            pv1=a
            pv2=b
            pv3=c
            a=a-d
            b=b-e
            c=c-f
            formatted_term = f"[({pv1})-({d})]x^2 & [({pv2})-({e})]x & [({pv3})-({f})]\n"
            steps.append(formatted_term)
            formatted_term = f"Final Equation : ({a})x^2 + ({b})x + ({c}) = 0\n"
            steps.append(formatted_term)
            result+= result1 + result2 +"".join(steps)
        discriminant = b**2 - 4*a*c
        square_root_discriminant = cmath.sqrt(discriminant)
        root1,root2 = find_roots(a, b, c)
        result += f"Using Sridharacharya's Formula to find the roots: [(-b ± √(b^2 - 4ac)) / (2a)]\n"
        result+= f"In above equation : a = {a} & b = {b} & c = {c}\n"
        if 4*a*c>=0 :
            result += f"Discriminant : {b**2}-{4*a*c} = {discriminant}\n"
        else :
            result += f"Discriminant : {b**2}+{abs(4*a*c)} = {discriminant}\n"
        result += f"Square root of Discriminant : ±√{discriminant} = {square_root_discriminant}\n"
        result += f"Root 1 and Root 2 : ({-b} ± {square_root_discriminant})/{2*a}\n"
        result += f"Root 1 : {root1}\nRoot 2 : {root2}\n\n"
        result += f"Additional Information for graph :-\n"
        result += f"Vertex : ({-b}/{2*a}),({-discriminant}/{4*a})\nVertex : ({(-b)/(2*a)}),({(-discriminant)/(4*a)})\n"
        result += f"Y-intercept of Equation : c = {c}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"
def convert_to_default_format(equation_str):
    # Split the equation string into left and right sides
    if '=' in equation_str :
        left_side, right_side = equation_str.split("=")
    
        # Remove spaces from both sides
        left_side = left_side.replace(" ", "")
        right_side = right_side.replace(" ", "")
        return left_side, right_side
    else :
        equation_str = equation_str.replace(" ", "")
        return equation_str,0
    
def extract_coefficients_and_constants(expression):
    a=b=c=i=0
    expression = expression.replace(' ', '')  # Remove spaces
    terms = re.split(r'(?=[+\-])', expression)  # Split by '+' and '-'
    steps = []
    invalid_terms = []

    for term in terms:
        if 'x' in term:
            
            # Extract coefficient and exponent
            match = re.match(r'([-+]?[\d.]*)(x(?:\^(\d+(\.\d+)?))?)?', term)
            if 'x^' in term:
                if 'x^2' in term:
                    if match:
                        
                        coefficient, _, _, _ = match.groups()
                        if coefficient == '+':
                            coefficient=1
                        elif coefficient == '-':
                            coefficient=-1
                        else :
                            coefficient = float(coefficient) if coefficient else 1.0
                        if a==0:
                            a+=coefficient
                        else :
                            i+=1
                            pv=a
                            a+=coefficient
                            formatted_term = f"Step {i}: [({pv}) + ({coefficient})]x = ({a})x^2\n"
                            steps.append(formatted_term)
                else :
                     invalid_terms.append(term)    
            elif 'x' in term:
                if match:
                        coefficient, _, _, _ = match.groups()
                        if coefficient == '+':
                            coefficient=1
                        elif coefficient == '-':
                            coefficient=-1
                        else :
                            coefficient = float(coefficient) if coefficient else 1.0
                            
                        if b==0:
                            b+=coefficient
                        else :
                            i+=1
                            pv=b
                            b+=coefficient
                            formatted_term = f"Step {i}: [({pv}) + ({coefficient})]x = ({b})x\n"
                            steps.append(formatted_term)
                
            else:
                invalid_terms.append(term)
        else:
            match2 = re.match(r'^[-+]?(\d*\.\d+|\d+\.\d*|\d+)([eE][-+]?\d+)?$',term)
            if match2 :
                if c==0 :
                        c+=float(term)
                else :
                        i+=1
                        pv=c
                        c+=float(term)
                        formatted_term = f"Step {i} : ({pv}) + ({term}) = ({c})\n"
                        steps.append(formatted_term)
            else :
                invalid_terms.append(term)
    formatted_term = f"Expression : ({a})x^2 + ({b})x + ({c})\n"
    steps.append(formatted_term)
    return "".join(steps),a,b,c

def extract_coefficients(equation):
    equation = re.sub(r'[a-z]', 'x', equation)
    match1 = re.match(r'([-+]?\d*\.*\d*)?[xX]\^2(\s*([-+]?\d*\.*\d*)?)?=\s*0', equation)
    match2 = re.search(r'([-+]?\d*)x\^2\s*([-+]?\d*)x\s*([-+]?\d*)=0', equation)
    
    if match1:
        a = float(match1.group(1)) if match1.group(1) else 1.0
        c = float(match1.group(2)) if match1.group(2) else 0.0
        b = 0
    elif match2:
        a = float(match2.group(1)) if match2.group(1) else 1.0
        d = match2.group(2)
        c = float(match2.group(3)) if match2.group(3) else 0.0

        if d == '+':
            b = 1.0
        elif d == '-':
            b = -1.0
        else:
            b = float(d) if d else 0.0
    return a, b, c

def find_roots(a, b, c):
    discriminant = cmath.sqrt(b**2 - 4*a*c)
    root1 = (-b + discriminant) / (2*a)
    root2 = (-b - discriminant) / (2*a)
    return root1, root2
def plot_quadratic(a, b, c):

     # Calculate the roots of the quadratic equation
    roots = find_roots(a, b, c)

    # Calculate the x-coordinate of the vertex
    vertex_x = -b / (2 * a)

    # Calculate the y-coordinate of the vertex
    vertex_y = (-(b**2 - 4 * a * c)) / (4 * a)

    # Determine the range of x-values to include vertex, roots, and y-intercept
    x_range = max(
        abs(roots[0] - vertex_x),
        abs(roots[1] - vertex_x),
        abs(0 - vertex_x)
    )

    # Create a list of x values with 100 points within the specified range
    x = [vertex_x + i * x_range / 100 for i in range(-150, 151)] 
    y = [a * xi**2 + b * xi + c for xi in x]  # Calculate the corresponding y values
    
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_linewidth(0.5)

    plt.plot(x, y, label=f"{a}x^2 + {b}x + {c}")
    plt.xlabel("x")
    plt.ylabel("y")
    
    # Plot roots and vertex
    if (b**2 - 4 * a * c)>=0:
        plt.scatter(roots, [0, 0], color='red', marker='o', label='Roots')
    plt.scatter(vertex_x, vertex_y, color='green', marker='o', label='Vertex')
    if c!=0 :
        plt.scatter(0, c, color='brown', marker='o', label='Y-Intercept')
    plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')
 
    # Add dotted lines from the vertex to the x-axis and y-axis
    plt.plot([vertex_x, vertex_x], [0, vertex_y], 'k--', linewidth=0.5)
    plt.plot([0, vertex_x], [vertex_y, vertex_y], 'k--', linewidth=0.5)

    
    
    plt.legend(loc='upper left')


    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    plt.clf()  # Clear the current figure
    ax.cla()   # Clear the current axis
    img_data = base64.b64encode(img_buf.read()).decode('utf8')
    return img_data

#Third Block