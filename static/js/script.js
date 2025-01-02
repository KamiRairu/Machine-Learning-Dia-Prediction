async function predict() {
    const glucose = document.getElementById('glucose').value;
    const bloodPressure = document.getElementById('bloodPressure').value;
    const bmi = document.getElementById('bmi').value;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                Glucose: parseFloat(glucose),
                BloodPressure: parseFloat(bloodPressure),
                BMI: parseFloat(bmi)
            })
        });

        const data = await response.json();
        if (data.error) {
            document.getElementById('result').innerText = `Error: ${data.error}`;
        } else {
            document.getElementById('result').innerText = `Prediction: ${data.prediction}`;
        }
    } catch (error) {
        document.getElementById('result').innerText = `Error: ${error.message}`;
    }
}
