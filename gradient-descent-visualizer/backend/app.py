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
        starting_point = float(data['starting_point'])
        learning_rate = float(data['learning_rate'])
        iterations = int(data['iterations'])

        # 1. วิเคราะห์ฟังก์ชันโดยใช้ SymPy
        x = sympy.Symbol('x')
        function = sympy.sympify(function_str)

        # 2. คำนวณอนุพันธ์
        derivative = sympy.diff(function, x)
        derivative_func = sympy.lambdify(x, derivative, 'numpy') #อนุพันธ์เชิงตัวเลข

        # 3. คำนวณ Gradient Descent
        x_values = [starting_point]
        y_values = []
        current_x = starting_point

        for i in range(iterations):
            current_y = function.evalf(subs={x: current_x}) #คำนวณค่าฟังก์ชันในแต่ละจุด
            y_values.append(float(current_y))
            gradient = derivative_func(current_x)
            current_x = current_x - learning_rate * gradient
            x_values.append(current_x)

        x_values = np.array(x_values[:-1])
        y_values = np.array(y_values)

        # 4. สร้างกราฟ (Matplotlib)
        x_plot = np.linspace(x_values.min()-2, x_values.max()+2, 400) #สร้างช่วงของค่า x สำหรับพล็อตกราฟ
        y_plot = [function.evalf(subs={x: val}) for val in x_plot]

        fig, ax = plt.subplots()
        ax.plot(x_plot, y_plot, label='Function')
        ax.scatter(x_values, y_values, color='red', label='Gradient Descent Path')
        ax.scatter(x_values[-1], y_values[-1], color = 'green', label = 'Minimum Point')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        ax.grid(True) #แสดงเส้นตาราง

        # 5. แปลงกราฟเป็น base64 encoded string
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8') #เพื่อนำไปแสดงผลใน html ได้

        #6. หาจุดต่ำสุด
        min_x = x_values[-1]
        min_y = y_values[-1]

        plt.close(fig)

        return jsonify({'plot': plot_url, 'min_x':str(min_x), 'min_y':str(min_y)}) #ส่งค่าพิกัดของจุดต่ำสุดกลับไปที่ frontend

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)