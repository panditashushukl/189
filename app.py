from flask import Flask, render_template, request, jsonify,send_file
from Simple import calculate_expression,steps_calculate_expression,plot_on_number_line
from Quadratic import find_quadratic_roots,quadratic_steps,plot_quadratic,get_abc
from Linearequation import solveEquation,plot_on_graph,solveequation2,solveequation3,plot_on_graph2,plot_on_graph3
from Functionswitharg import function_with_arg,plot_on_number_line2


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')
    
@app.route('/BhaskarAcharya', methods=['GET', 'POST'])
def home():
    result = None
    img_data = None
    steps = None
    if request.method == 'POST':       
        calculation_type = request.form.get('calculationType')
        expression = request.form.get('userInput')
        try:
            if calculation_type == "simple":
                result,_ =calculate_expression(expression)
                if result.imag == 0:
                    result=result.real
                steps = steps_calculate_expression(expression)
                img_data = plot_on_number_line(result)  
                result=f"Answer = {result}"           
                
            elif calculation_type == "linear1":
                result,steps = solveEquation(expression)
                img_data = plot_on_graph(result) 
                            
            elif calculation_type == "quadratic":
                result = find_quadratic_roots(expression)
                steps = quadratic_steps(expression)
                a,b,c = get_abc(expression)
                img_data = plot_quadratic(a,b,c)
                
            elif calculation_type == "functions":
                result,steps,_ = function_with_arg(expression) 
                if result.imag == 0:
                    result=result.real
                img_data = plot_on_number_line2(result,expression)
                result=f"Answer = {result}"  

            elif calculation_type == "linear2":
                if ',' in expression :
                    expression1, expression2 = expression.split(",")
                result,steps = solveequation2(expression1, expression2)
                img_data = plot_on_graph2(expression1,expression2)

            elif calculation_type == "linear3":
                if ',' in expression :
                    expression1, expression2, expression3 = expression.split(",")
                result,steps = solveequation3(expression1, expression2,expression3)
                img_data =plot_on_graph3(expression1, expression2,expression3)  
            response = {
                'result': result, 
                'steps': steps,  
                'graph': img_data  
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({
                'result': "Error: Invalid calculation",
                'steps': "There was an error processing your request.",
                'graph': ""
            })
    return render_template('solver.html')

@app.route('/calculate-native', methods=['POST'])
def calculate():
    data = request.json
    calculation_type = data.get('calculationType')
    user_input = data.get('userInput')

    steps = None
    img_data = None

    if calculation_type == "simple":
        result, _ = calculate_expression(user_input)
        steps = steps_calculate_expression(user_input)
        history = f" Provided Expression :\n {user_input}\n\n Result:\n {result} \n\n Steps: \n {steps}"
        if isinstance(result, (int, float, complex)):
            img_data = plot_on_number_line(result)
            if result.imag != 0:
                result = f"Real part: {result.real}\n Imaginary part: {result.imag}"
            else:
                result = f"Answer = {result.real}"
        else:
            result = result 
        return jsonify({'input' : f"Your Input Expression : {user_input}",'result': result, 'steps': steps or "", 'graph': img_data or "", 'history': history})

    elif calculation_type == "linear1":
        result, steps = solveEquation(user_input)
        history = f" Provided Expression :\n {user_input}\n\n Result:\n {result} \n\n Steps: \n {steps}"
        img_data = plot_on_graph(result)
        return jsonify({'input' : f"Your Input Expression : {user_input}",'result': result, 'steps': steps or "", 'graph': img_data or "", 'history': history})

    elif calculation_type == "quadratic":
        result = find_quadratic_roots(user_input)
        steps = quadratic_steps(user_input)
        history = f" Provided Expression :\n {user_input}\n\n Result:\n {result} \n\n Steps: \n {steps}"
        a, b, c = get_abc(user_input)
        img_data = plot_quadratic(a, b, c)
        return jsonify({'input' :f"Your Input Expression : {user_input}",'result': result, 'steps': steps or "", 'graph': img_data or "", 'history': history})

    elif calculation_type == "functions":
        result, steps, _ = function_with_arg(user_input)
        if result.imag == 0:
            result=result.real
        history = f" Provided Expression :\n {user_input}\n\n Result:\n {result} \n\n Steps: \n {steps}"
        img_data = plot_on_number_line2(result,user_input)
        result=f"Answer = {result}" 
        return jsonify({'input' : f"Your Input Expression : {user_input}",'result': result, 'steps': steps or "", 'graph': img_data or "", 'history': history})

    elif calculation_type == "linear2":
        if ',' in user_input :
            expression1, expression2 = user_input.split(",")
        result, steps = solveequation2(expression1, expression2)
        history = f" Provided Expression :\n {user_input}\n\n Result:\n {result} \n\n Steps: \n {steps}"
        img_data = plot_on_graph2(expression1, expression2)
        return jsonify({'input' : f"Your Input Expression : {expression1} \n {expression2}",'result': result, 'steps': steps or "", 'graph': img_data or "", 'history': history})

    elif calculation_type == "linear3":
        if ',' in user_input :
            expression1, expression2,expression3 = user_input.split(",")
        result, steps = solveequation3(expression1, expression2, expression3)
        history = f" Provided Expression :\n {user_input}\n\n Result:\n {result} \n\n Steps: \n {steps}"
        img_data = plot_on_graph3(expression1, expression2, expression3)
        return jsonify({'input' : f"Your Input Expression : {expression1} \n {expression2} \n {expression3}" ,'result': result, 'steps': steps or "", 'graph': img_data or "", 'history': history})

    else:
        return jsonify({'error': "Invalid calculation type"})

@app.route('/DigiMathsBot', methods=['GET', 'POST'])
def bot():
    return render_template('bot.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)