from flask import Flask, request, jsonify
import numpy as np
import sympy as sp
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load history from file
HISTORY_FILE = "history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

history_data = load_history()

# Define function and its derivative
x = sp.Symbol('x')
define_function = x**2 - 4*x + 4  # Default function

def compute_gradient(f_expr):
    df_dx = sp.diff(f_expr, x)
    return sp.lambdify(x, df_dx, 'numpy')

def compute_function(f_expr):
    return sp.lambdify(x, f_expr, 'numpy')

# Gradient Descent Algorithm
def gradient_descent(f_prime, f, start_x, learning_rate=0.1, max_iters=50, tolerance=1e-6):
    x_values = [start_x]
    y_values = [f(start_x)]
    x_curr = start_x
    
    for _ in range(max_iters):
        grad = f_prime(x_curr)
        x_next = x_curr - learning_rate * grad
        
        x_values.append(x_next)
        y_values.append(f(x_next))
        
        if abs(x_next - x_curr) < tolerance:
            break
        
        x_curr = x_next
    
    return x_values, y_values

@app.route('/gradient_descent', methods=['POST'])
def run_gradient_descent():
    data = request.get_json()
    expr_str = data.get('function', 'x**2 - 4*x + 4')
    start_x = float(data.get('start_x', 5.0))
    learning_rate = float(data.get('learning_rate', 0.1))
    max_iters = int(data.get('max_iters', 50))
    
    # Parse function
    f_expr = sp.sympify(expr_str)
    f = compute_function(f_expr)
    df = compute_gradient(f_expr)
    
    # Run Gradient Descent
    x_vals, y_vals = gradient_descent(df, f, start_x, learning_rate, max_iters)
    
    # Save to history
    history_entry = {
        "function": expr_str,
        "start_x": start_x,
        "learning_rate": learning_rate,
        "max_iters": max_iters,
        "result_x": x_vals[-1],
        "result_y": y_vals[-1]
    }
    history_data.append(history_entry)
    save_history(history_data)
    
    return jsonify({"x_values": x_vals, "y_values": y_vals})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(history_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
