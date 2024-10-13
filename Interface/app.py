from flask import Flask, render_template, request

app = Flask(__name__)

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
        age = request.form.get('age')
        gender = request.form.get('gender')
        hypertension = request.form.get('hypertension')
        heart_disease = request.form.get('heart_disease')
        avg_glucose = request.form.get('avg_glucose')
        bmi = request.form.get('bmi')
        marital_status = request.form.get('marital_status')
        residence_type = request.form.get('residence_type')
        smoking_status = request.form.get('smoking_status')
        work_type = request.form.get('work_type')
        
        # Pass the collected data to the result page
        return render_template('result.html', 
                               name=name, 
                               age=age, 
                               gender=gender, 
                               hypertension=hypertension, 
                               heart_disease=heart_disease, 
                               avg_glucose=avg_glucose, 
                               bmi=bmi, 
                               marital_status=marital_status, 
                               residence_type=residence_type, 
                               smoking_status=smoking_status, 
                               work_type=work_type)
    return render_template('input.html')

# Login page
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
