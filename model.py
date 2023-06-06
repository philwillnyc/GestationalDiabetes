"""Generates a Logistic Regression model for the gestational diabetes data."""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression

from joblib import dump, load

df = pd.read_excel('gestationalDiabetes.xlsx', index_col = 0)

#Deal with nan.

#HDL and BMI.
HDL_mean = np.mean(df['HDL'])
BMI_mean = np.mean(df['BMI'])
df['HDL'].fillna(HDL_mean, inplace = True)
df['BMI'].fillna(BMI_mean, inplace = True)

#Sys BP.
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
bp = df[['Sys BP','Dia BP']].dropna()
reg.fit(bp[['Dia BP']], bp[['Sys BP']])
predicted_bp = reg.predict(df[['Dia BP']])
predicted_bp = [x[0] for x in predicted_bp] #need to flatten so that fillna can handle it
df['Sys BP'] = df['Sys BP'].fillna(pd.Series(predicted_bp))

#All measurements typically done during an annual physical.
df_physical = df[['Dia BP',
                            'Sys BP',
                            'HDL',
                           'BMI', 
                            'Age',
                            'Prediabetes',
                            'Class Label(GDM /Non GDM)']]

#Train a Logistic regression model.
X = df_physical[['Dia BP',
                            'Sys BP',
                            'HDL',
                           'BMI', 
                            'Age',
                            'Prediabetes',]]
y = df_physical[['Class Label(GDM /Non GDM)']]
X_train, X_test, y_train, y_test  = train_test_split(X,y)
model = LogisticRegression(max_iter = 200)
model.fit(X_train,y_train)

#Save the model.
dump(model,'model.joblib')

#Create the predictor.
def predict(dia_bp, sys_bp, hdl, bmi, age, prediabetes):
    """Input physical parameters and returns a probability of gestational diabetes."""
    model = load('model.joblib')
    _, result = model.predict_proba([[dia_bp,sys_bp,hdl,bmi,age,prediabetes]])[0]
    return result
