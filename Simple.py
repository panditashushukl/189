import cmath
import re #import of regular Expression module parse input Expression
import matplotlib.pyplot as plt
from io import BytesIO
import base64


#For first Block
def convert_brackets(expression):
    expression = expression.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
    return expression

def apply_operation(operand1, operator, operand2=None):
    step = ''
    if operator == '+':
        step = f"{operand1} {operator} {operand2}\n{operand1 + operand2}"
        return operand1 + operand2, step
    elif operator == '-':
        step = f"{operand1} {operator} {operand2}\n{operand1 - operand2}"
        return operand1 - operand2, step
    elif operator == '*':
        step = f"{operand1} {operator} {operand2}\n{operand1 * operand2}"
        return operand1 * operand2, step
    elif operator == '/':
        if operand2 == 0:
            raise ValueError("Division by zero is not allowed")
        step = f"{operand1} {operator} {operand2}\n{operand1 / operand2}"
        return operand1 / operand2, step
    elif operator == '%':
        operand1_real = int(operand1.real)
        operand1_imag = int(operand1.imag)
        operand2_real = int(operand2.real)
        operand2_imag = int(operand2.imag)
        if operand1_imag != 0 and operand2_imag != 0:
            step = f"{operand1_imag}j {operator} {operand2_imag}j\n{operand1_imag % operand2_imag}j"
            result=complex(0, operand1_imag % operand2_imag)
            return result, step
            
        else : 
            step = f"{operand1_real} {operator} {operand2_real}\n{operand1_real % operand2_real}"
            return operand1_real % operand2_real, step
        

    elif operator == '^':
        if operand2 == 0.5 :
            step = f"{operand1} {operator} {operand2}\n{cmath.sqrt(operand1)}"
            return cmath.sqrt(operand1), step
        elif operand2 == 0.3333333333333333 :
            if operand1 < 0:
                operand1 = abs(operand1)
                step = f"{operand1} {operator} {operand2} * (-1)\n{(operand1)**(1/3)*(-1)}"
                return (operand1)**(1/3)*(-1), step
            else :
                step = f"{operand1} {operator} {operand2}\n{(operand1)**(1/3)}"
                return (operand1)**(1/3), step
        elif operand2 == 0.25 :
            if operand1 < 1 :
                operand1 = abs(operand1)
                step = f"{operand1} {operator} {operand2}\n{(operand1)**(1/4)*(cmath.sqrt(-1))}"
                return ((operand1)**(1/4)*(cmath.sqrt(-1))), step
            else :
                step = f"{operand1} {operator} {operand2}\n{(operand1)**(1/4)}"
                return (operand1)**(1/4), step
        else :   
            step = f"{operand1} {operator} {operand2}\n{operand1 ** operand2}"
            return operand1 ** operand2, step
    elif operator == '√':
        step = f"{operator}{operand1}\n{cmath.sqrt(operand1)}"
        return cmath.sqrt(operand1), step
    else:
        raise ValueError("Invalid operator")

def calculate_expression(expression):
    expression = convert_brackets(expression)
    pattern = r'(\d+\.?\d*|[+\-*/%^()√ji])'
    tokens = re.findall(pattern, expression)

    i = 0
    while i < len(tokens):
        if (tokens[i].isdigit() or (tokens[i].count('.') == 1 and tokens[i].replace('.', '').isdigit())) and i < len(tokens) - 1 and (tokens[i + 1] in ('j', 'i')):
            # Check if we have a complex number
            complex_token = tokens[i] + 'j'
            tokens[i] =(complex_token)
            del tokens[i + 1]
        i += 1

    operator_stack = []
    operand_stack = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3, '√': 4}
    steps = []  # List to store steps

    for i, token in enumerate(tokens):
        
        if token[0].isdigit():
            operand_stack.append(complex(token))
        elif token[0] in "+-*/%^":
            while (operator_stack and operator_stack[-1] in "+-*/%^√" and
                    precedence[token[0]] <= precedence[operator_stack[-1]]):
                operator = operator_stack.pop()
                if operator == '√':
                    operand1 = operand_stack.pop()
                    result, step = apply_operation(operand1, operator)
                else:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result, step = apply_operation(operand1, operator, operand2)
                operand_stack.append(result)
                steps.append(step)
            operator_stack.append(token[0])
        elif token[0] == '(':
            if i + 2 < len(tokens) and tokens[i + 1] == '-' and tokens[i + 2].isdigit():
                j = i + 2
                while j < len(tokens) and (tokens[j].isdigit() or tokens[j] == '.'):
                    j += 1
                operand = -complex("".join(tokens[i + 2:j]))
                operand_stack.append(operand)
                del tokens[i + 1:j]
            operator_stack.append(tokens[i])
            i += 1
            #operator_stack.append(token[0])
        elif token[0] == ')':
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                if operator == '√':
                    operand1 = operand_stack.pop()
                    result, step = apply_operation(operand1, operator)
                else:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result, step = apply_operation(operand1, operator, operand2)
                operand_stack.append(result)
                steps.append(step)
            operator_stack.pop()
        elif token[0] == '√':
            if i < len(tokens) - 1 and tokens[i + 1] == '-' and i < len(tokens) - 2:
                operator_stack.append(token)
                operand_stack.append(-complex(tokens[i + 2]))
                if i < len(tokens) - 3:
                    tokens[i] = tokens[i + 3]  # Update the current token
                    del tokens[i + 1:i + 3]  # Remove the used tokens
                else:
                    del tokens[i:i + 3]  # Remove the used tokens if there are no more tokens
            else:
                #operator_stack.append(token)            
                operator_stack.append(token[0])

    # Handle remaining operators
    while operator_stack:
        operator = operator_stack.pop()
        if operator == '√':
                    operand1 = operand_stack.pop()
                    result, step = apply_operation(operand1, operator)
        else:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result, step = apply_operation(operand1, operator, operand2)
        operand_stack.append(result)
        steps.append(step)
    return operand_stack[0], steps
def steps_calculate_expression(expression):
    _, steps = calculate_expression(expression)
    
    steps_str = ""
    for i, step in enumerate(steps, start=1):
        steps_str += f"Step {i}: {step}\n\n"
    return steps_str

def plot_on_number_line(number):
    if number.imag == 0:
        number = float(number.real)
        
        # Create a new figure and axis for the complex plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(number, 0, color='red', label=(number, 0))
        ax.set_xlabel('Real Part (X-axis)')
        ax.set_ylabel('Imaginary Part (Y-axis)')
        ax.set_title('Real Number Plot')

         # Show the point name above the point
        ax.text(number, 0.01, f"({number},0)", ha='center', fontsize=12, color='red')

        

        # Convert the plot to a base64 encoded image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        
        # Clear the previous axis to avoid runtime errors
        plt.clf()  # Clear the current figure
        ax = plt.gca()
        ax.cla()  # Clear the current axis
    else:
        inumber = float(number.imag)
        number = float(number.real)
        
        # Create a new figure and axis for the complex plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(number, inumber, color='red', label=(number, inumber))
        ax.set_xlabel('Real Part (X-axis)')
        ax.set_ylabel('Imaginary Part (Y-axis)')
        ax.set_title('Complex Number Plot')
        
        # Show the point name above the point
        ax.text(number, inumber + 0.1, f"({number}, {inumber})", ha='center', fontsize=12, color='red')


        # Convert the complex plot to a base64 encoded image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        
        # Clear the previous axis to avoid runtime errors
        plt.clf()  # Clear the current figure
        ax = plt.gca()
        ax.cla()  # Clear the current axis

    return image_data



#For first Block

