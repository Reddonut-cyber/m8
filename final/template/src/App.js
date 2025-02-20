import "./index.css";
import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const API_URL = "http://127.0.0.1:5000";

function App() {
  const [func, setFunc] = useState("x**2 - 4*x + 4");
  const [startX, setStartX] = useState(5);
  const [learningRate, setLearningRate] = useState(0.1);
  const [iterations, setIterations] = useState(50);
  const [data, setData] = useState(null);

  const handleSubmit = async () => {
    const response = await fetch(`${API_URL}/gradient_descent`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ function: func, start_x: startX, learning_rate: learningRate, max_iters: iterations }),
    });
    const result = await response.json();
    setData(result);
  };

  return (
    <div className="bg-gray-100 min-h-screen flex justify-center items-center p-6">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-3xl">
        <h1 className="text-2xl font-bold text-gray-800 mb-4 text-center">Gradient Descent Calculator</h1>

        <div className="grid grid-cols-2 gap-4">
          <input className="border p-2 rounded-md w-full" type="text" placeholder="Function" value={func} onChange={(e) => setFunc(e.target.value)} />
          <input className="border p-2 rounded-md w-full" type="number" placeholder="Start X" value={startX} onChange={(e) => setStartX(Number(e.target.value))} />
          <input className="border p-2 rounded-md w-full" type="number" placeholder="Learning Rate" value={learningRate} onChange={(e) => setLearningRate(Number(e.target.value))} />
          <input className="border p-2 rounded-md w-full" type="number" placeholder="Iterations" value={iterations} onChange={(e) => setIterations(Number(e.target.value))} />
        </div>

        <button onClick={handleSubmit} className="w-full bg-blue-500 text-white py-2 rounded-md mt-4 hover:bg-blue-600 transition">Run Gradient Descent</button>

        {data && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold text-gray-700 text-center">Results</h2>
            <div className="p-4 bg-gray-50 rounded-md">
              <Line data={{
                labels: data.x_values.map((_, i) => i),
                datasets: [{ label: "Gradient Descent Progress", data: data.y_values, borderColor: "red", fill: false }]
              }} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
