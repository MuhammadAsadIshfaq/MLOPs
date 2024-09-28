import streamlit as st
import numpy as np
import requests
import json

# Define the URI of your deployed model
scoring_uri = "http://37988042-599d-43e9-9024-13d85a100f2c.southeastasia.azurecontainer.io/score"  
headers = {"Content-Type": "application/json"}

# Set up the Streamlit app layout
st.title("Diabetes Prediction App")

st.markdown("""
    Please enter the following values:
""")

# Collecting inputs from the user
pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0, step=1)
glucose = st.number_input("Glucose", min_value=0, max_value=300, value=120)
blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=70)
skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20)
insulin = st.number_input("Insulin", min_value=0, max_value=1000, value=80)
bmi = st.number_input("BMI", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
diabetes_pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=5.0, value=0.5, step=0.01)
age = st.number_input("Age", min_value=0, max_value=120, value=30)

# Input data array
input_data = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]

# Define a function to make the API call for prediction
def predict(input_data):
    input_data_json = json.dumps({"data": [input_data]})
    response = requests.post(scoring_uri, data=input_data_json, headers=headers)
    if response.status_code == 200:
        result = json.loads(response.json())
        return result["result"][0]
    else:
        return None

# Predict button
if st.button("Predict"):
    with st.spinner("Predicting..."):
        prediction = predict(input_data)
        if prediction is not None:
            if prediction == 1:
                st.success("The model predicts that the patient have diabetes.")
            else:
                st.success("The model predicts that the patient have no diabetes.")
        else:
            st.error("There was an error in the prediction process. Please try again later.")
