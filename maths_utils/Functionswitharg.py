import re
import math
from maths_utils.Simple import steps_calculate_expression,calculate_expression
import matplotlib.pyplot as plt
from io import BytesIO
import base64
# Define a simple LinkedList class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
					
def function_value(func, arg,i): 
    if func == "cos":
        value = str(math.cos(math.radians(arg)))
        step = f"Step {i} :cos({arg}) = {value}\n"
    elif func == "sin":
        value = str(math.sin(math.radians(arg)))
        step = f"Step {i} :sin({arg}) = {value}\n"
    elif func == "tan":
        value = str(math.tan(math.radians(arg))) 
        step = f"Step {i} :tan({arg}) = {value}\n"
    elif func == "cosec" :
        value = str(1/(math.sin(math.radians(arg))))
        step = f"Step {i} :sin({arg}) = {value}\n"
    elif func == "sec" :
        value = str(1/(math.cos(math.radians(arg))))
        step = f"Step {i} :sin({arg}) = {value}\n"
    elif func == "cot" :
        value = str(1/(math.tan(math.radians(arg))))
        step = f"Step {i} :sin({arg}) = {value}\n"
    elif func == "log":
        value = str(math.log10(arg))
        step = f"Step {i} :log({arg}) = {value}\n"

    return value,step		
					
def function_with_arg(expression)  :
    steps = []
    i=0
    # Tokenize the expression using regular expressions
    tokens = re.findall(r'[-+]?\d*\.\d+|\d+|[-+*/()]|[a-zA-Z]+\(\d+\)', expression)
    # Initialize a linked list
    linked_list = LinkedList()
    step = f"Value Each Function :-\n"
    steps.append(step)
    for token in tokens:
        if (token.startswith("cos(") or token.startswith("sin(") or 
                token.startswith("tan(") or token.startswith("log(") or 
                token.startswith("cosec(") or token.startswith("sec(") or
                token.startswith("cot(")  ):
            i+=1
            # Extract the function name and argument
            func, arg = re.match(r'([a-zA-Z]+)\((\d+)\)', token).groups()
            arg = float(arg)
            value,step = function_value(func, arg,i)
        else:
            value = token
            step=""
        linked_list.append(value)
        steps.append(step)
    # Build the result string
    result = ""
    current = linked_list.head
    while current:
        result += current.data
        current = current.next
    if i>1 :
        step = f"\nCalculation of Values :-\n"
        steps.append(step)
    # Display the result as a string
    solution,_= calculate_expression(result)
    steps_str = steps_calculate_expression(result)
    steps= "".join(steps) + steps_str
    return solution,steps,tokens

def plot_on_number_line2(number,expression):
        i=0
        number = float(number.real)
        # Create a new figure and axis for the complex plot
        fig, ax = plt.subplots(figsize=(10, 6))
        _,_,tokens=function_with_arg(expression)
        for token in tokens:
            if (token.startswith("cos(") or token.startswith("sin(") or 
                token.startswith("tan(") or token.startswith("log(") or 
                token.startswith("cosec(") or token.startswith("sec(") or
                token.startswith("cot(")  ):
                i+=1
                # Extract the function name and argument
                func, arg = re.match(r'([a-zA-Z]+)\((\d+)\)', token).groups()
                arg = float(arg)
                x_min = math.radians(arg) -  math.pi
                x_max = math.radians(arg) +  math.pi
                step = 0.1
                x_plot = [x_min + i * step for i in range(int((x_max - x_min) / step))]
                if func == "cos":
                    y_plot = [math.cos(xi) for xi in x_plot]
                    plt.plot(x_plot, y_plot, label=f"Function : [{func}({arg})]")
                    value = math.cos(math.radians(arg))
                    plt.scatter(math.radians(arg), value, color='blue', label=(value, 0))
                elif func == "sin":
                    y_plot = [math.sin(xi) for xi in x_plot]
                    plt.plot(x_plot, y_plot, label=f"Function : [{func}({arg})]")
                    value= math.sin(math.radians(arg))
                    plt.scatter(math.radians(arg), value, color='green', label=(value, 0))
                elif func == "tan":
                    y_plot = [math.tan(xi) for xi in x_plot]
                    plt.plot(x_plot, y_plot, label=f"Function : [{func}({arg})]")
                    value = math.tan(math.radians(arg))
                    ax.scatter(math.radians(arg), value, color='black', label=(value, 0))
                elif func == "cosec":
                    y_plot = [1/(math.sin(xi) for xi in x_plot)]
                    plt.plot(x_plot, y_plot, label=f"Function : [{func}({arg})]")
                    value = 1/(math.sin(math.radians(arg)))
                    ax.scatter(math.radians(arg), value, color='green', label=(value, 0))
                elif func == "sec":
                    y_plot = [1/(math.cos(xi) for xi in x_plot)]
                    plt.plot(x_plot, y_plot, label=f"Function : [{func}({arg})]")
                    value = 1/(math.cos(math.radians(arg)))
                    ax.scatter(math.radians(arg), value, color='green', label=(value, 0))
                elif func == "cot":
                    y_plot = [1/(math.tan(xi) for xi in x_plot)]
                    plt.plot(x_plot, y_plot, label=f"Function : [{func}({arg})]")
                    value = 1/(math.tan(math.radians(arg)))
                    ax.scatter(math.radians(arg), value, color='green', label=(value, 0))
                elif func == "log":
                    arg = int(arg)
                    x_min = arg - 1
                    x_max = arg + 1
                    step = 0.1

                    x_plot = [x_min + i * step for i in range(int((x_max - x_min) / step))]
                    y_plot = [1 / math.log(xi) for xi in x_plot]
                    plt.plot(x_plot, y_plot, label=f"Function : [{func}({arg})]")
                    value = 1/(math.log(arg))
                    ax.scatter(arg, value, color='green', label=(value, 0))
					
                    ax.scatter(math.radians(arg), value, color='black', label=(value, 0))
        if func == "log":
              ax.scatter(arg, number, color='red', label=(number, 0))          
        else :
            ax.scatter(math.radians(arg), number, color='red', label=(number, 0))
        ax.set_xlabel('(X-axis)')
        ax.set_ylabel('(Y-axis)')
        ax.set_title('Function Plot')

        # Show the point name above the point
        # ax.text(number, 0.01, f"({number},0)", ha='center', fontsize=12, color='red')

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
