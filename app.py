from flask import Flask, render_template, request, session
from flask_session import Session

from model import predict

#Create the flask app.

app = Flask(__name__)

#Set up individual sessions so multiple users don't conflict. 

app.secret_key = '123456789'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
server_session = (Session(app))

#Computational functions.

def compute_bmi(height,weight):
    """Height in inches, weight in lbs."""
    return 703*(weight/(height**2))

def check_prediabetes(a1c,glucose):
    return int(glucose > 100 or a1c > 5.6)

#Rendering. 

@app.route('/', methods=['GET'])
def home():
    session['prediction'] = ''
    return render_template(
                'predict.html', 
                prediction = session['prediction'],
                    )

@app.route('/', methods=['GET','POST'])
def compute():
    r = request.form
    dia_bp = r['diastolic']
    sys_bp = r['systolic']
    hdl = r['hdl']
    bmi = compute_bmi(r['height'],r['weight'])
    age = r['age']
    prediabetes = check_prediabetes(r['a1c'],[r['glucose']])
    prediction = predict(dia_bp,sys_bp,hdl,bmi,age,prediabetes)
    return render_template(
                'predict.html', 
                prediction = session['prediction'],
                    )

app.run(debug = True)