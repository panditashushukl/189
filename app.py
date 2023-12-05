from flask import Flask, render_template, request, jsonify,send_file
from Simple import calculate_expression,steps_calculate_expression,plot_on_number_line
from Quadratic import find_quadratic_roots,quadratic_steps,plot_quadratic,get_abc
from Linearequation import solveEquation,plot_on_graph,solveequation2,solveequation3,plot_on_graph2,plot_on_graph3
from Functionswitharg import function_with_arg,plot_on_number_line2



app = Flask(__name__)
calculation_history = []
chat_history = []

@app.route('/')
def index():

    return render_template('index.html',calculation_history=calculation_history)


@app.route('/calculate', methods=['GET', 'POST'])
def home():
    
    result = None
    img_data = None

    if request.method == 'POST':
        
        
        calculation_type = request.form.get('calculationType')
        try:
            if calculation_type == "simple":
                expression = request.form.get('userInput')
                # Implement simple calculation logic here
                result,steps =calculate_expression(expression)
                steps_str = steps_calculate_expression(expression)
                img_data = plot_on_number_line(result)             
                calculation_history.append((f"Input Expression : \n{expression}",f"Result : \n{result}",steps_str)) 
                
                
            elif calculation_type == "linear1":
                expression = request.form.get('userInput1')
                # Implement linear equation solution logic here
                result,steps = solveEquation(expression)
                img_data = plot_on_graph(result) 
                calculation_history.append((f"Input Expression : \n{expression}",f"Result : \n{result}",steps))   
                            
            elif calculation_type == "quadratic":
                expression = request.form.get('userInput')
                # Implement quadratic equation solution logic here
                result = find_quadratic_roots(expression)
                steps = quadratic_steps(expression)
                a,b,c = get_abc(expression)
                img_data = plot_quadratic(a,b,c)
                calculation_history.append((f"Input Expression : \n{expression}",f"Result : \n{result}",steps))
                
            elif calculation_type == "functions":
                expression = request.form.get('userInput')
                # Implement functions problem solution logic here
                result,step,_ = function_with_arg(expression) 
                img_data = plot_on_number_line2(result,expression)
                calculation_history.append((f"Input Expression : \n{expression}",f"Result : \n{result}",step))

            elif calculation_type == "linear2":
                # Implement scientific calculation logic here
                expression1 = request.form.get('userInput1')
                expression2 = request.form.get('userInput2')
                result,steps = solveequation2(expression1, expression2)
                img_data = plot_on_graph2(expression1,expression2)
                calculation_history.append((f"Input Expression : \n{expression1}\n{expression2}", f"Result : \n{result}",steps))

            elif calculation_type == "linear3":
                expression1 = request.form.get('userInput1')
                expression2 = request.form.get('userInput2')
                expression3 = request.form.get('userInput3')
                result,step = solveequation3(expression1, expression2,expression3)
                img_data =plot_on_graph3(expression1, expression2,expression3)
                calculation_history.append((f"Input Expression : \n{expression1}\n{expression2}\n{expression3}", f"Result : \n{result}",step))

            else :
                result = "Error: Invalid calculation"
                return result
        
        except Exception as e:
            print("Error:", e)

        
    return render_template('index.html', result=result, calculation_history=calculation_history,img_data=img_data)




@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']

    # Here you can process the user input and generate a response
    response = home(user_input)

    # Add the user's input and the response to the chat history
    chat_history.append({'user': user_input, 'response': response})

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

