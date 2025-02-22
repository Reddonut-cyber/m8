let gradientPoints = [];

document.getElementById('calculateBtn').addEventListener('click', function() {
    const functionStr = document.getElementById('functionInput').value;
    const startingPointX = document.getElementById('startingPointX').value;
    const learningRate = document.getElementById('learningRate').value;
    const iterations = document.getElementById('iterations').value;

    const requestBody = {
        function: functionStr,
        starting_point_x: startingPointX,
        learning_rate: learningRate,
        iterations: iterations
    };

    fetch('http://127.0.0.1:5000/gradient_descent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('plotContainer').innerHTML = `<p class='text-danger'>Error: ${data.error}</p>`;
        } else {
            document.getElementById('gradientPlot').src = "data:image/png;base64," + data.plot;
            document.getElementById('gradientPlot').style.display = 'block';
            document.getElementById('minPoint').style.display = 'block';
            document.getElementById('minPoint').innerHTML = `<strong>Minimum Point:</strong> x = ${data.min_x}, f(x) = ${data.min_z}`;
            gradientPoints = data.gradient_path;
            document.getElementById('iterationSlider').max = gradientPoints.length - 1;
        }
    });
});

document.getElementById('iterationSlider').addEventListener('input', function() {
    const index = parseInt(this.value, 10);
    document.getElementById('iterationValue').innerText = `Iteration: ${index}`;
    if (gradientPoints.length > 0) {
        document.getElementById('minPoint').innerHTML = `<strong>Step ${index}:</strong> x = ${gradientPoints[index].x}, f(x) = ${gradientPoints[index].z}`;
    }
});
