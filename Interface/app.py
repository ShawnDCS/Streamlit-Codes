import pickle
from flask import Flask, render_template, request, redirect
import joblib
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the stroke prediction model
model = joblib.load("stroke_model.pkl")

# Check the type of the loaded model
print("Loaded model type:", type(model))

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Input page where users submit medical details
@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        age = float(request.form.get('age'))
        gender = request.form.get('gender')

        # Convert hypertension and heart disease responses to numerical values
        hypertension_value = 1 if request.form.get('hypertension') == 'yes' else 0
        heart_disease_value = 1 if request.form.get('heart_disease') == 'yes' else 0

        # Retrieve other form data
        avg_glucose = float(request.form.get('avg_glucose'))
        bmi = float(request.form.get('bmi'))
        marital_status = request.form.get('marital_status')
        residence_type = request.form.get('residence_type')
        smoking_status = request.form.get('smoking_status')
        work_type = request.form.get('work_type')

        # Prepare input data for prediction
        input_data = [[age, hypertension_value, heart_disease_value, avg_glucose, bmi, smoking_status, marital_status, work_type]]
        columns = ['AGE', 'HYPERTENSION', 'HEART_DISEASE', 'AVG_GLUECOSE_LEVEL', 'BMI', 'SMOKING_STATUS', 'MARITAL_STATUS', 'WORK_TYPE']
        input_df = pd.DataFrame(input_data, columns=columns)

        # Print input data for debugging
        print("Input Data for Prediction:", input_data)

        # Predict using the model
        try:
            prediction = model.predict(input_df)
            stroke_prediction = 'Yes' if prediction[0] == 1 else 'No'
        except Exception as e:
            print("Error during prediction:", e)
            stroke_prediction = f"Error in prediction: {e}"

        # Pass the collected data and prediction to the result page
        return render_template('result.html',
                               name=name,
                               age=age,
                               gender=gender,
                               hypertension=hypertension_value,
                               heart_disease=heart_disease_value,
                               avg_glucose=avg_glucose,
                               bmi=bmi,
                               marital_status=marital_status,
                               residence_type=residence_type,
                               smoking_status=smoking_status,
                               work_type=work_type,
                               stroke_prediction=stroke_prediction)

    return render_template('input.html')

# Login page
@app.route('/login')
def login():
    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        return redirect('/')
    return render_template('signup.html')

# About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Information page
@app.route('/info')
def info():
    return render_template('info.html')

# Contact Us page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
