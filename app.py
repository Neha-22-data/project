import pandas as pd
import joblib
from flask import (Flask, url_for, render_template,request)
from forms import InputForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"

model = joblib.load('model.joblib')

@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html', title = "Home")

@app.route('/predict', methods=['GET','POST'])
def predict():
    form = InputForm()
    
    if form.validate_on_submit():
        x_new = pd.DataFrame(dict(
            airline=[form.airline.data],
            date_of_journey=[form.date_of_journey.data.strftime("%Y-%m-%d")],
            source=[form.source.data],
            destination=[form.destination.data],
            dep_time=[form.dep_time.data.strftime("%H:%M:%S")],
            arrival_time=[form.arrival_time.data.strftime("%H:%M:%S")],
            duration=[form.duration.data],
            total_stops=[form.total_stops.data],
            additional_info=[form.additional_info.data]
        ))
        # print(x_new[0])
        prediction = model.predict(x_new)[0]
        message = f"The predicted price is {prediction:,.0f} INR!"
        
    else:
        message = "Please provide the valid input details!"

    return render_template("predict.html", title="Predict", form = form, output=message)
    
# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     form = InputForm()
#     message = ""

#     print("Request Method:", request.method)  # Debugging print statement
#     if request.method == 'POST':
#         print("Form Submitted")  # Debugging print statement
#         if form.validate_on_submit():
#             print("Form Validated")  # Debugging print statement
#             try:
#                 x_new = pd.DataFrame(dict(
#                     airline=[form.airline.data],
#                     data_of_journey=[form.data_of_journey.data.strftime("%Y-%m-%d")],
#                     source=[form.source.data],
#                     destination=[form.destination.data],
#                     dep_time=[form.dep_time.data.strftime("%H:%M:%S")],
#                     arrival_time=[form.arrival_time.data.strftime("%H:%M:%S")],
#                     duration=[form.duration.data],
#                     total_stops=[form.total_stops.data],
#                     additional_info=[form.additional_info.data]
#                 ))
#                 print("Input DataFrame:", x_new)  # Debugging print statement
#                 prediction = model.predict(x_new)[0]
#                 message = f"The predicted price is {prediction:,.0f} INR!"
#             except Exception as e:
#                 message = f"An error occurred: {str(e)}"
#         else:
#             message = "Please provide valid input details!"
#     else:
#         print("Form Not Submitted or GET Request")  # Debugging print statement

#     print("Form Validation Status:", form.validate_on_submit())  # Debugging print statement
#     print("Form Errors:", form.errors)  # Debugging print statement
#     print("Output Message:", message)  # Debugging print statement

#     return render_template("predict.html", title="Predict", form=form, output=message)


if __name__ == ('__main__'):
    app.run(debug=True)