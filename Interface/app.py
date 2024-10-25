import pickle
from flask import Flask, render_template, request
import joblib
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the model
# lda_model is not yet trained
# with open("stroke_model.pkl", "rb") as f:
#     model = pickle.load(f)

model = joblib.load("stroke_model.pkl")

# Check the type of the loaded model
print("Loaded model type:", type(model))  # Print the type of the loaded model

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
        input_data = [[age, hypertension_value, heart_disease_value, avg_glucose, bmi, smoking_status, marital_status, work_type]] # Disregard gender, residence type, and marital status
        columns = ['AGE', 'HYPERTENSION', 'HEART_DISEASE', 'AVG_GLUECOSE_LEVEL', 'BMI', 'SMOKING_STATUS', 'MARITAL_STATUS', 'WORK_TYPE']
        input_df = pd.DataFrame(input_data, columns=columns)

        # Print input data for debugging
        print("Input Data for Prediction:", input_data)  # Print input data for debugging
        
        # Predict using the model
        try:
            print("Data Types for Prediction:")
            print("Age:", type(age))
            print("Hypertension Value:", type(hypertension_value))
            print("Heart Disease Value:", type(heart_disease_value))
            print("Average Glucose:", type(avg_glucose))
            print("BMI:", type(bmi))

            prediction = model.predict(input_df)  # Predict stroke risk
            print(prediction)
            stroke_prediction = 'Yes' if prediction[0] == 1 else 'No'  # Interpret prediction
        except Exception as e:
            print("Error during prediction:", e)  # Print error if prediction fails
            stroke_prediction = f"Error in prediction: {e}"  # Display the actual error message

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
                               stroke_prediction=stroke_prediction)  # Pass the stroke prediction to the template

    return render_template('input.html')

# Login page
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
