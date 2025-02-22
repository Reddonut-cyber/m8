from flask import Flask, request, jsonify
import numpy as np
import sympy
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/gradient_descent', methods=['POST'])
def gradient_descent():
    try:
        data = request.get_json()
        function_str = data['function']
        starting_point_x = float(data['starting_point_x'])
        learning_rate = float(data['learning_rate'])
        iterations = int(data['iterations'])

        # วิเคราะห์ฟังก์ชัน
        x = sympy.Symbol('x')
        function = sympy.sympify(function_str)

        # คำนวณอนุพันธ์
        derivative_x = sympy.diff(function, x)
        grad_x_func = sympy.lambdify(x, derivative_x, 'numpy')
        func_eval = sympy.lambdify(x, function, 'numpy')

        # คำนวณ Gradient Descent
        x_values, y_values = [starting_point_x], []
        current_x = starting_point_x

        for _ in range(iterations):
            y_values.append(func_eval(current_x))
            grad_x = grad_x_func(current_x)
            current_x -= learning_rate * grad_x
            x_values.append(current_x)

        # หาจุดต่ำสุด
        min_x = x_values[-1]
        min_z = func_eval(min_x)

        # สร้างกราฟ
        fig, ax = plt.subplots()
        X = np.linspace(min(x_values)-1, max(x_values)+1, 400)
        Y = [func_eval(val) for val in X]
        ax.plot(X, Y, label='Function')
        ax.scatter(x_values[:-1], y_values, color='red', label='Gradient Descent Path')
        ax.scatter(min_x, min_z, color='green', label='Minimum Point')

        ax.set_xlabel('X')
        ax.set_ylabel('f(x)')
        ax.legend()

        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return jsonify({
            'plot': plot_url,
            'min_x': str(min_x),
            'min_z': str(min_z),
            'gradient_path': [{'x': x_values[i], 'z': y_values[i]} for i in range(len(y_values))]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
