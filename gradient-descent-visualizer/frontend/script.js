document.getElementById('calculateBtn').addEventListener('click', function() {
    const functionStr = document.getElementById('functionInput').value;
    const startingPoint = document.getElementById('startingPoint').value;
    const learningRate = document.getElementById('learningRate').value;
    const iterations = document.getElementById('iterations').value;

    fetch('http://127.0.0.1:5000/gradient_descent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            function: functionStr,
            starting_point: startingPoint,
            learning_rate: learningRate,
            iterations: iterations
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('plotContainer').innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            document.getElementById('plotContainer').innerHTML = `<img src="data:image/png;base64,${data.plot}" alt="Gradient Descent Plot">`;
            document.getElementById('minPoint').innerText = `Minimum Point (x): ${data.min_x}, f(x): ${data.min_y}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('plotContainer').innerHTML = `<p>Error: ${error}</p>`;
    });
});