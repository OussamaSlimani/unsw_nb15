from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

# Load the trained models
lgb_model_unsw_15_loaded = joblib.load('lgb_model_unsw_15.pkl')
print("Model 1 loaded successfully.")

lgb_model_cic_ids_2018_loaded = joblib.load('lgb_model_cic_ids_2018.pkl')
print("Model 2 loaded successfully.")

# Define attack categories based on the dataset description
attack_categories_unsw_15 = {
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

attack_categories_cic_ids_2018 = {
    0: 'Benign',
    1: 'Bot',
    2: 'DDOS attack-HOIC',
    3: 'DDoS attacks-LOIC-HTTP',
    4: 'DoS attacks-GoldenEye',
    5: 'DoS attacks-Hulk',
    6: 'DoS attacks-SlowHTTPTest',
    7: 'DoS attacks-Slowloris',
    8: 'FTP-BruteForce',
    9: 'Infiltration',
    10: 'SSH-Bruteforce'
}

# Define the prediction endpoint for the UNSW 15 model
@app.route('/predict/unsw_15', methods=['POST'])
def predict_unsw_15():
    data = request.json
    try:
        input_df = pd.DataFrame([data])
        prediction = lgb_model_unsw_15_loaded.predict(input_df)
        predicted_class_name = attack_categories_unsw_15.get(prediction[0], "Unknown")
        return jsonify({'predicted_class': predicted_class_name, 'class_id': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the prediction endpoint for the CIC IDS 2018 model
@app.route('/predict/cic_ids_2018', methods=['POST'])
def predict_cic_ids_2018():
    data = request.json
    try:
        input_df = pd.DataFrame([data])
        prediction = lgb_model_cic_ids_2018_loaded.predict(input_df)
        predicted_class_name = attack_categories_cic_ids_2018.get(prediction[0], "Unknown")
        return jsonify({'predicted_class': predicted_class_name, 'class_id': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the home route with the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json_data = request.form.get('json_data')
        model_type = request.form.get('model_type')
        try:
            # Parse the JSON data
            data = pd.read_json(json_data, typ='series').to_dict()
            # Make prediction based on the selected model
            if model_type == 'unsw_15':
                response = predict_unsw_15()
            else:
                response = predict_cic_ids_2018()
            return render_template('index.html', result=response.get_json(), json_data=json_data)
        except Exception as e:
            return render_template('index.html', error=str(e), json_data=json_data)
    return render_template('index.html', result=None)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
