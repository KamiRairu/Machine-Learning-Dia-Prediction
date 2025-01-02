import joblib
import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Constants
MODEL_PATH = 'model.pkl'  # Path to the pre-trained model

# Function to load the pre-trained model
def load_model(model_path):
    if os.path.exists(model_path):
        return joblib.load(model_path)  # Load the pre-trained model
    else:
        raise FileNotFoundError("Model file not found")  # Raise error if model not found

model = load_model(MODEL_PATH)  # Load the model when the app starts

# Home route to render the frontend
@app.route('/')
def home():
    return render_template('index.html')  # Render your HTML template

# API route to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json  # Expecting JSON input for the features

        required_features = ['Glucose', 'BloodPressure', 'BMI']
        # Check if any required feature is missing or empty
        missing_or_empty = [f for f in required_features if not input_data.get(f)]
        if missing_or_empty:
            return jsonify({'error': f'Missing or empty features: {", ".join(missing_or_empty)}'}), 400

        # Convert input data to a DataFrame (required for prediction)
        new_data = pd.DataFrame([input_data])

        # Make the prediction using the pre-trained model
        prediction = model.predict(new_data)
        result = 'Positive for diabetes' if prediction[0] == 1 else 'Negative for diabetes'

        return jsonify({'prediction': result})  # Return the prediction as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error if something goes wrong

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode