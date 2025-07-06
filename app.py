from flask import Flask, render_template, request, jsonify,send_file
from maths_utils.Simple import calculate_expression,steps_calculate_expression,plot_on_number_line
from maths_utils.Quadratic import solve_quadratic
from maths_utils.Linearequation import solveEquation,plot_on_graph,solveequation2,solveequation3,plot_on_graph2,plot_on_graph3
from maths_utils.Functionswitharg import function_with_arg,plot_on_number_line2

def process_calculation(data):
    try:
        expression = data.get('userInput')
        calculation_type = data.get('calculationType')

        result = None
        img_data = None
        steps = None

        if calculation_type == "simple":
            result, _ = calculate_expression(expression)
            if result.imag == 0:
                result = result.real
            steps = steps_calculate_expression(expression)
            img_data = plot_on_number_line(result)
            result = f"Answer = {result}"

        elif calculation_type == "linear1":
            result, steps = solveEquation(expression)
            img_data = plot_on_graph(result)

        elif calculation_type == "quadratic":
            return solve_quadratic(expression)

        elif calculation_type == "functions":
            result, steps, _ = function_with_arg(expression)
            if result.imag == 0:
                result = result.real
            img_data = plot_on_number_line2(result, expression)
            result = f"Answer = {result}"

        elif calculation_type == "linear2":
            if ',' in expression:
                expression1, expression2 = expression.split(",")
            result, steps = solveequation2(expression1, expression2)
            img_data = plot_on_graph2(expression1, expression2)

        elif calculation_type == "linear3":
            if ',' in expression:
                expression1, expression2, expression3 = expression.split(",")
            result, steps = solveequation3(expression1, expression2, expression3)
            img_data = plot_on_graph3(expression1, expression2, expression3)

        return {
            'result': result,
            'steps': steps,
            'graph': img_data
        }
        

    except Exception as e:
        return {
            'result': "Error: Invalid calculation",
            'steps': "There was an error processing your request.",
            'graph': ""
        }


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')
    
@app.route('/BhaskarAcharya', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('solver.html')  # when browser visits the page

    # Handle JSON POST
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    
    response = process_calculation(data)
    return jsonify(response)


@app.route('/calculate-native', methods=['POST'])
def calculate():
    data = request.json
    response = process_calculation(data)
    return jsonify(response)

@app.route('/DigiMathsBot', methods=['GET', 'POST'])
def bot():
    return render_template('bot.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)