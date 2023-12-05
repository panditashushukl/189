import re   
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from mpl_toolkits import mplot3d
#For Linear equation in one Variable

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

       
def extract_coefficients_and_constants(expression,i):
    constants = []
    if expression=="0":
        a=b=0
        return "\n".join(constants),a,b,i
    else :
       
        a=b=0
        expression = expression.replace(' ', '')  # Remove spaces
        terms = re.split(r'(?=[+\-])', expression)  # Split by '+' and '-'
        invalid_terms = []
    
        for term in terms:
            if 'x' in term:
                
                # Extract coefficient and exponent
                match = re.match(r'([-+]?[\d.]*)(x(?:\^(\d+(\.\d+)?))?)?', term)
                if 'x^' in term:
                        invalid_terms.append(term)    
                elif 'x' in term:
                     if match:
                        
                        coefficient, _,_,_ = match.groups() # variable, exponent, float_exponent
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
                            formatted_term = f"Step {i}: [({pv}) + ({coefficient})]x = ({a})x"
                            constants.append(formatted_term)
                        
                    
                else:
                    invalid_terms.append(term)
            else:
                match2 = re.match(r'^[-+]?(\d*\.\d+|\d+\.\d*|\d+)([eE][-+]?\d+)?$',term)
                if match2 :
                    
                    if b==0 :
                        b+=float(term)
                    else :
                        i+=1
                        pv=b
                        b+=float(term)
                        formatted_term = f"Step {i} : ({pv}) + ({term}) = ({b})"
                        constants.append(formatted_term)
                    
                else :
                    invalid_terms.append(term)
        formatted_term = f"Simplified Expression :({a})x + ({b})\n"
        constants.append(formatted_term)
        return "\n".join(constants),a,b,i
def solve(a,b,i):
    constants = []
    i+=1
    formatted_term = f"Step {i} : x = [-({b})]/({a})"
    constants.append(formatted_term)
    i+=1
    formatted_term = f"Step {i}: x = ({-b/a})"
    constants.append(formatted_term)
    return f"x = ({-b/a})","\n".join(constants)

def solveEquation(expression):
    i=0
    constants = []
     # Replace any variable from 'a' to 'z' with 'x'
    expression= re.sub(r'[a-z]', 'x', expression)
    # Define a regular expression pattern for the equation ax + b = 0
    equation_pattern = r'^\s*([-+]?[0-9]*\.?[0-9]+)?\s*?x\s*([-+]\s*[0-9]*\.?[0-9]+)?\s*=\s*0\s*$'

    # Check if the input matches the pattern
    if re.match(equation_pattern, expression):
        # Parse the coefficients 'a' and 'b' from the input
        match = re.match(equation_pattern, expression)
        a = float(match.group(1) or 1)
        b = float(match.group(2) or 0)
        formatted_term = f"Equation : [({a})x + ({b}) = 0]"
        constants.append(formatted_term)
        ans,result=solve(a,b,i)
        return ans,result
        
    else :
            l,r=convert_to_default_format(expression)
            result1,a,b,i = extract_coefficients_and_constants(l,i)
            result2,c,d,i = extract_coefficients_and_constants(r,i)
            pv1=a
            pv2=b
            a=a-c
            b=b-d
            i+=1
            formatted_term = f"Step {i} :[({pv1})-({c})]x= ({a})x & [({pv2})-({d})= ({b})]"
            constants.append(formatted_term)
            formatted_term = f"Final Equation : [({a})x + ({b}) = 0]\n"
            constants.append(formatted_term)
            result3 = "\n".join(constants)
            ans,result=solve(a,b,i)
            result_combined = result1 + result2 + result3 + result
            return ans,result_combined


def plot_on_graph(number):
        
    # Create a figure and axes
    x = [number, number]
    y = [-20, 20]
    
    plt.figure(figsize=(8, 6))
    ax = plt.gca()

    plt.plot(x, y, label=f"{number}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    
    # Convert the plot to a base64 encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode()
    
    # Clear the previous axis to avoid runtime errors
    plt.clf()  # Clear the current figure
    ax = plt.gca()
    ax.cla()  # Clear the current axis
    # Create a figure and axes
    x = [number, number]
    y = [-20, 20]
    
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    return image_data


#For Linear Equation in one Variables


#For Linear Equation in two Variables


def convert_to_default_format2(equation_str):
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
def extract_coefficients_and_constants2(expression,i):
    steps = []
    if expression=="0":
        a=b=c=0
        steps=""
        return "".join(steps),a,b,c,i
    a=b=c=0
    expression = expression.replace(' ', '')  # Remove spaces
    terms = re.split(r'(?=[+\-])', expression)  # Split by '+' and '-'
    invalid_terms = []

    for term in terms:
        if 'x' in term:
            
            # Extract coefficient and exponent
            match = re.match(r'([-+]?[\d.]*)(x(?:\^(\d+(\.\d+)?))?)?', term)
            if 'x^' in term:
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
                    if a==0:
                        a+=coefficient
                    else :
                        i+=1
                        pv=a
                        a+=coefficient
                        formatted_term = f"Step {i}: [({pv}) + ({coefficient})]x = ({a})x\n"
                        steps.append(formatted_term)
                
            else:
                invalid_terms.append(term)
        elif 'y' in term:
            
            # Extract coefficient and exponent
            match = re.match(r'([-+]?[\d.]*)(y(?:\^(\d+(\.\d+)?))?)?', term)
            if 'y^' in term:
                invalid_terms.append(term)    
            elif 'y' in term:
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
                    formatted_term = f"Step {i}: [({pv}) + ({coefficient})]y = ({b})y\n"
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
    formatted_term = f"Expression : ({a})x + ({b})y + ({c})\n"
    steps.append(formatted_term)
    return "".join(steps),a,b,c,i
def get_abc2(expression,i) :
    # Define the updated linear equation pattern
    pattern = r'(-?\d*)x?\s*([+-]?\s*\d*)y?\s*([+-]?\s*\d+)\s*=\s*0'
    expression=expression.replace(" ", "")
    match = re.match(pattern, expression)
    
    if match:
            a = float(match.group(1) or 1)  # Default 'a' to 1 if not provided
            b = float(match.group(2) or 0)  # Default 'b' to 1 if not provided
            c = float(match.group(3) or 0)
            return a,b,c,"",i
    else:

        l,r=convert_to_default_format2(expression)
        result1,a,b,c,i= extract_coefficients_and_constants2(l,i)
        result2,d,e,f,i= extract_coefficients_and_constants2(r,i)
        a=a-d
        b=b-e
        c=c-f
        result = result1 + result2
        return a,b,c,result,i
def determinant_solution2(a1,b1,c1,a2,b2,c2):
                steps = []
                formatted_term = f"Standard form Equation1: [({a1})x + ({b1})y + ({c1}) = 0]\n"
                steps.append(formatted_term)
                formatted_term = f"Standard form Equation2: [({a2})x + ({b2})y + ({c2}) = 0]\n"
                steps.append(formatted_term)
                # Calculate the determinants
                det = a1 * b2 - a2 * b1
                formatted_term = f"determinant  = a1 * b2 - a2 * b1\n"
                steps.append(formatted_term)
                formatted_term = f"determinant  = [({a1}) * ({b2}) - ({a2}) * ({b1})]\n"
                steps.append(formatted_term)
                formatted_term = f"determinant  = [{det}]\n"
                steps.append(formatted_term)
                det_x = c1 * b2 - c2 * b1
                formatted_term = f"determinant of x = c1 * b2 - c2 * b1\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of x  = [({c1}) * ({b2}) - ({c2}) * ({b1})]\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of x  = [{det_x}]\n"
                steps.append(formatted_term)
                det_y = a1 * c2 - a2 * c1
                formatted_term = f"determinant of y = a1 * c2 - a2 * c1\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of y  = [({a1}) * ({c2}) - ({a2}) * ({c1})]\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of y  = [{det_y}]\n"
                steps.append(formatted_term)
                return det, det_x, det_y,"".join(steps)
     
def solveequation2(equation1,equation2):
                i=0
                steps = []
                a1, b1, c1,step1,i = get_abc2(equation1,i)
                a2, b2, c2,step2,i = get_abc2(equation2,i)
                det, det_x, det_y,step3=determinant_solution2(a1,b1,c1,a2,b2,c2)
               

                # Check if the system has a unique solution or is inconsistent
                if det != 0:
                    # Calculate the solutions
                    x = det_x / det
                    y = det_y / det
                    formatted_term = f"x = det_x / det\n"
                    steps.append(formatted_term)
                    formatted_term = f"x = ({det_x}) / ({det}) = ({x})\n"
                    steps.append(formatted_term)
                    y = det_y / det
                    formatted_term = f"y = det_y / det\n"
                    steps.append(formatted_term)
                    formatted_term = f"y = ({det_y}) / ({det}) = ({y})\n"
                    steps.append(formatted_term)
                    step = step1 + step2 + step3 + "".join(steps)
                    return f"x = {x}\ny = {y}",step
                else:
                    if det_x == 0 and det_y == 0:
                        formatted_term = f"Since determinant x & y is 0 Hence the system of equations has infinitely many solutions\n"
                        steps.append(formatted_term)
                        step = step1 + step2 + step3 + "".join(steps)
                        return "The system of equations has infinitely many solutions",step
                    else:
                        formatted_term = f"Since one of determinant x & y is 0 Hence the system of equations has no solution.\n"
                        steps.append(formatted_term)
                        step = step1 + step2 + step3 + "".join(steps)
                        return "The system of equations has no solution.",step


def plot_on_graph2(equation1,equation2):
    i=0
    a1, b1, c1,_ ,_= get_abc2(equation1,i)
    a2, b2, c2,_ ,_= get_abc2(equation2,i)
    det, det_x, det_y,_=determinant_solution2(a1,b1,c1,a2,b2,c2)
    if det != 0:
        x=det_x/det
        y=det_y/det
        x_plot = [x-20,x+20]
        y_plot1 = [y - ((-a1 * x - c1)/b1), y + ((-a1 * x - c1)/b1)]
        y_plot2 = [y - ((-a2 * x - c2)/b2), y + ((-a2 * x - c2)/b2)]
        

    else    :
            x_plot = [-20,20]
            y_plot1 = [(-a1 * (-20) - c1) / b1, (-a1 * (20) - c1) / b1]
            y_plot2 = [(-a2 * (-20) - c2) / b2, (-a2 * (20) - c2) / b2]


    plt.figure(figsize=(8, 6))
    ax = plt.gca()

    plt.plot(x_plot, y_plot1, label=f"Equation 1: [({a1})x+({b1})y+({c1})=0]")
    plt.plot(x_plot, y_plot2, label=f"Equation 2: [({a2})x+({b2})y+({c2})=0]")
    plt.xlabel("x")
    plt.ylabel("y")
    if det != 0:
        plt.scatter(x, y, color='green', marker='o', label='Intersection Point')
    plt.legend(loc='upper left')

    
    # Convert the plot to a base64 encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode()
    
    # Clear the previous axis to avoid runtime errors
    plt.clf()  # Clear the current figure
    ax = plt.gca()
    ax.cla()  # Clear the current axis

    return image_data

#For Linear Equation in two Variables


#For Linear Equation in three Variables

def convert_to_default_format3(equation_str):
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
def extract_coefficients_and_constants3(expression,i):
    steps = []
    if expression=="0":
        a=b=c=d=0
        steps=""
        return "".join(steps),a,b,c,d,i
    a=b=c=d=0
    expression = expression.replace(' ', '')  # Remove spaces
    terms = re.split(r'(?=[+\-])', expression)  # Split by '+' and '-'
    invalid_terms = []

    for term in terms:
        if 'x' in term:
            
            # Extract coefficient and exponent
            match = re.match(r'([-+]?[\d.]*)(x(?:\^(\d+(\.\d+)?))?)?', term)
            if 'x^' in term:
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
                    if a==0:
                        a+=coefficient
                    else :
                        i+=1
                        pv=a
                        a+=coefficient
                        formatted_term = f"Step {i}: [({pv}) + ({coefficient})]x = ({a})x\n"
                        steps.append(formatted_term)
                
            else:
                invalid_terms.append(term)
        elif 'y' in term:
            
            # Extract coefficient and exponent
            match = re.match(r'([-+]?[\d.]*)(y(?:\^(\d+(\.\d+)?))?)?', term)
            if 'y^' in term:
                invalid_terms.append(term)    
            elif 'y' in term:
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
                    formatted_term = f"Step {i}: [({pv}) + ({coefficient})]y = ({b})y\n"
                    steps.append(formatted_term)
                
            else:
                invalid_terms.append(term)
        if 'z' in term:
            
            # Extract coefficient and exponent
            match = re.match(r'([-+]?[\d.]*)(y(?:\^(\d+(\.\d+)?))?)?', term)
            if 'z^' in term:
                invalid_terms.append(term)    
            elif 'z' in term:
                coefficient, _, _, _ = match.groups()
                if coefficient == '+':
                    coefficient=1
                elif coefficient == '-':
                    coefficient=-1
                else :
                    coefficient = float(coefficient) if coefficient else 1.0
                    
                if c==0:
                    c+=coefficient
                else :
                    i+=1
                    pv=c
                    c+=coefficient
                    formatted_term = f"Step {i}: [({pv}) + ({coefficient})]z = ({c})z\n"
                    steps.append(formatted_term)
                
            else:
                invalid_terms.append(term)
        else:
            match2 = re.match(r'^[-+]?(\d*\.\d+|\d+\.\d*|\d+)([eE][-+]?\d+)?$',term)
            if match2 :
                if d==0 :
                    d+=float(term)
                else :
                    i+=1
                    pv=d
                    d+=float(term)
                    formatted_term = f"Step {i} : ({pv}) + ({term}) = ({d})\n"
                    steps.append(formatted_term)
            else :
                invalid_terms.append(term)
    formatted_term = f"Expression : ({a})x + ({b})y + ({c})z + ({d})\n"
    steps.append(formatted_term)
    return "".join(steps),a,b,c,d,i
def get_abc3(expression,i) :
    # Define the updated linear equation pattern
    pattern = r'(-?\d*)x?\s*([+-]?\s*\d*)y?\s*([+-]?\s*\d*)z?\s*([+-]?\s*\d+)\s*=\s*0'
    expression=expression.replace(" ", "")
    match = re.match(pattern, expression)
    
    if match:
            a = float(match.group(1) or 1)  # Default 'a' to 1 if not provided
            b = float(match.group(2) or 0)  # Default 'b' to 1 if not provided
            c = float(match.group(3) or 0)
            d = float(match.group(4) or 0)
            return a,b,c,d,"",i
    else:

        l,r=convert_to_default_format3(expression)
        result1,a,b,c,d,i= extract_coefficients_and_constants3(l,i)
        result2,e,f,g,h,i= extract_coefficients_and_constants3(r,i)
        print(a,b,c,d,e,f,g,h)
        a=a-e
        b=b-f
        c=c-g
        d=d-h
        print(a,b,c,d,e,f,g,h)
        result = result1 + result2
        return a,b,c,d,result,i
def determinant_solution3(a1,b1,c1,d1,a2,b2,c2,d2,a3, b3, c3,d3):
                steps = []
                formatted_term = f"Standard form Equation1: [({a1})x + ({b1})y + ({c1})z + ({d1}) = 0]\n"
                steps.append(formatted_term)
                formatted_term = f"Standard form Equation2: [({a2})x + ({b2})y + ({c2})z + ({d2}) = 0]\n"
                steps.append(formatted_term)
                formatted_term = f"Standard form Equation3: [({a3})x + ({b3})y + ({c3})z + ({d3}) = 0]\n"
                steps.append(formatted_term)

                # Calculate the determinants
                det = a1 * (b2 * c3 - b3 * c2) - b1 * (a2 * c3 - a3 * c2) + c1 * (a2 * b3 - a3 * b2)
                formatted_term = f"determinant  = a1 * (b2 * c3 - b3 * c2) - b1 * (a2 * c3 - a3 * c2) + c1 * (a2 * b3 - a3 * b2)\n"
                steps.append(formatted_term)
                formatted_term = f"determinant=[({a1})*[({b2})*({c3})-({b3})*({c2})] - ({b1})*[({a2})*({c3})-({a3})*({c2})) + ({c1})*[({a2})*({b3})-({a3})*({b2})]\n"
                steps.append(formatted_term)
                formatted_term = f"determinant  = [{det}]\n"
                steps.append(formatted_term)
                det_x = d1 * (b2 * c3 - b3 * c2) - b1 * (d2 * c3 - d3 * c2) + c1 * (d2 * b3 - d3 * b2)
                formatted_term = f"determinant of x = d1 * (b2 * c3 - b3 * c2) - b1 * (d2 * c3 - d3 * c2) + c1 * (d2 * b3 - d3 * b2)\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of x=[({d1})*[({b2})*({c3})-({b3})*({c2})]-({b1})*[({d2})*({c3})-({d3})*({c2})]+({c1})*[({d2})*({b3})-({d3})*({b2})]\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of x  = [{det_x}]\n"
                steps.append(formatted_term)
                det_y = a1 * (d2 * c3 - d3 * c2) - d1 * (a2 * c3 - a3 * c2) + c1 * (a2 * d3 - a3 * d2)
                formatted_term = f"determinant of y = a1 * (d2 * c3 - d3 * c2) - d1 * (a2 * c3 - a3 * c2) + c1 * (a2 * d3 - a3 * d2)\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of y=[({a1})*[({d2})*({c3})-({d3})*({c2})]-({d1})*[({a2})*({c3})-({a3})*({c2})]+({c1})*[({a2})*({d3})-({a3})*({d2})]]\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of y  = [{det_y}]\n"
                steps.append(formatted_term)
                det_z = a1 * (b2 * d3 - b3 * d2) - b1 * (a2 * d3 - a3 * d2) + d1 * (a2 * b3 - a3 * b2)
                formatted_term = f"determinant of z = a1 * (b2 * d3 - b3 * d2) - b1 * (a2 * d3 - a3 * d2) + d1 * (a2 * b3 - a3 * b2)\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of z=[({a1})*(({b2})*({d3})-({b3})*({d2}))-({b1})*(({a2})*({d3})-({a3})*({d2}))+({d1})*(({a2})*({b3})-({a3})*({b2}))]\n"
                steps.append(formatted_term)
                formatted_term = f"determinant of z  = [{det_z}]\n"
                steps.append(formatted_term)
                return det,det_x,det_y,det_z,"".join(steps)
     
def solveequation3(equation1,equation2,equation3):
 # Parse the two equations
                steps = []
                i=0
                a1, b1, c1,d1,step1,i = get_abc3(equation1,i)
                a2, b2, c2,d2,step2,i = get_abc3(equation2,i)
                a3, b3, c3,d3,step3,i = get_abc3(equation3,i)
                det, det_x, det_y,det_z,step4=determinant_solution3(a1,b1,c1,d1,a2,b2,c2,d2,a3, b3, c3,d3)
               

                # Check if the system has a unique solution or is inconsistent
                if det != 0:
                    # Calculate the solutions
                    x = det_x / det
                    y = det_y / det
                    formatted_term = f"x = det_x / det\n"
                    steps.append(formatted_term)
                    formatted_term = f"x = ({det_x}) / ({det}) = ({x})\n"
                    steps.append(formatted_term)
                    y = det_y / det
                    formatted_term = f"y = det_y / det\n"
                    steps.append(formatted_term)
                    formatted_term = f"y = ({det_y}) / ({det}) = ({y})\n"
                    steps.append(formatted_term)
                    z = det_z / det
                    formatted_term = f"z = det_z / det\n"
                    steps.append(formatted_term)
                    formatted_term = f"y = ({det_z}) / ({det}) = ({z})\n"
                    steps.append(formatted_term)
                    step = step1 + step2 + step3 + step4 + "".join(steps)
                    return f"x = {x}\ny = {y}\nz = {z}",step
                else:
                    if det_x == 0 and det_y == 0 and det_z == 0:
                        formatted_term = f"Since determinant x & y & z is 0 Hence the system of equations has infinitely many solutions\n"
                        steps.append(formatted_term)
                        step = step1 + step2 + step3 + step4 + "".join(steps)
                        return "The system of equations has infinitely many solutions",step
                    else:
                        formatted_term = f"Since one of determinant x & y & z is 0 Hence the system of equations has no solution.\n"
                        steps.append(formatted_term)
                        step = step1 + step2 + step3 + step4 + "".join(steps)
                        return "The system of equations has no solution.",step


def plot_on_graph3(equation1,equation2,equation3):
    i=0
    a1, b1, c1,d1,_,_ = get_abc3(equation1,i)
    a2, b2, c2,d2,_,_ = get_abc3(equation2,i)
    a3, b3, c3,d3,_,_ = get_abc3(equation3,i)

    det, det_x, det_y,det_z,_=determinant_solution3(a1,b1,c1,d1,a2,b2,c2,d2,a3, b3, c3,d3)
    if det != 0:
        x=det_x/det
        y=det_y/det
        z=det_z/det
        x_plot = [x-20,x+20]
        y_plot = [y-20,y+20]
        z_plot1 = [z - ((-a1 * x - b1 * y- d1)/c1), z + ((-a1 * x - b1 * y- d1)/c1)]
        z_plot2 = [z - ((-a2 * x - b2 * y- d2)/c2), z + ((-a2 * x - b2 * y- d2)/c2)]
        z_plot3 = [z - ((-a3 * x - b3 * y- d3)/c3), z + ((-a3 * x - b3 * y- d3)/c3)]

        

    else    :
            x_plot = [-20,20]
            y_plot = [-20,20]
            z_plot1 = [((-a1 * (-20) - b1 * (-20)- d1)/c1), ((-a1 * 20 - b1 * 20- d1)/c1)]
            z_plot2 = [((-a2 * (-20)- b2 * (-20)- d2)/c2), ((-a2 * 20 - b2 * 20- d2)/c2)]
            z_plot3 = [((-a3 * (-20) - b3 * (-20)- d3)/c3), ((-a3 * 20- b3 * 20- d3)/c3)]


    plt.figure(figsize=(8, 6))

    # syntax for 3-D projection
    ax = plt.axes(projection ='3d')


    ax.plot3D(x_plot, y_plot, z_plot1, 'green',label=f"Equation 1: [({a1})x+({b1})y+({c1})z+({d1})=0]")
    ax.plot3D(x_plot, y_plot, z_plot2, 'red',label=f"Equation 2:[({a2})x+({b2})y+({c2})z+({d2})=0]")
    ax.plot3D(x_plot, y_plot, z_plot3, 'blue',label=f"Equation 3:[({a3})x+({b3})y+({c3})z+({d3})=0]")
    
    if det != 0:
        ax.scatter(x, y, z, color='green', marker='o', label='Intersection Point')
    plt.legend(fontsize='small', bbox_to_anchor=(1, 1), loc='center right')

    
    # Convert the plot to a base64 encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode()
    
    # Clear the previous axis to avoid runtime errors
    plt.clf()  # Clear the current figure
    ax = plt.gca()
    ax.cla()  # Clear the current axis

    return image_data
#For Linear Equation in three Variables
