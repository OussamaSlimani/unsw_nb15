from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
lgb_model_loaded = joblib.load('lgb_model.pkl')
print("Model loaded successfully.")

# Define attack categories based on the dataset description
attack_categories = {
    0: 'analysis',
    1: 'backdoor',
    2: 'backdoors',
    3: 'dos',
    4: 'exploits',
    5: 'fuzzers',
    6: 'generic',
    7: 'normal',
    8: 'reconnaissance',
    9: 'shellcode',
    10: 'worms'
}

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.json

    # Convert JSON to DataFrame
    try:
        input_df = pd.DataFrame([data])
    except Exception as e:
        return jsonify({'error': f'Invalid data format: {e}'}), 400

    # Make prediction
    try:
        prediction = lgb_model_loaded.predict(input_df)
        predicted_class_name = attack_categories.get(prediction[0], "Unknown")
    except Exception as e:
        return jsonify({'error': f'Prediction error: {e}'}), 500

    # Return result as JSON
    return jsonify({
        'predicted_class': predicted_class_name,
        'class_id': int(prediction[0])
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
