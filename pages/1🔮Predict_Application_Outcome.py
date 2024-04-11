"""

PERM Application Analysis Web Application Prediction Page

"""

import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import random

# Loading model and encoder
model = joblib.load('./data/model.joblib')
encoders = joblib.load('./data/label_encoders.joblib')

# Create Title
st.title("PERM Application Prediction")
st.markdown("## Applicant's Information")

# Load options from files
def load_options(file):
    with open('./data/' + file + '.txt', 'r') as file:
        options = file.readlines()
        options = [option.strip() for option in options]
    return options

# Autocomplete selectbox simulation
def find_user_input(file, item, emoji):
    options  = load_options(file)
    search_term = st.text_input(emoji + "**Input keywords to search your " + item + ".**")
    filtered_options = [option for option in options if search_term.lower() in option.lower()]
    filtered_options.append("Others")
    return st.selectbox(emoji + "**Select a " + item + ". Choose \"Other\" if it is not on the list.**", filtered_options)

# Loading images
pass_img = Image.open('./image/pass.jpg')
fail_img= Image.open('./image/fail.jpg')

# Build application information
parameter_input_values = [] 
parameter_list=["employer" , "education_level" ,"citizenship", "class_of_admission",
                "agent_firm" , "job_title" , "experience_level" , "wage_level" ]
wage_level_list = ['Level 1: Below 50K', 'Level 2: 50K-75K', 'Level 3: 75K-100K', 'Level 4: 100K-150K','Level 5: Above 150K']
education_list = ['High School', "Associate's", "Bachelor's", "Master's", 'Doctorate', 'Other']
experience_list = ['Level 1: 0-12 months', 'Level 2: 13-36 months', 'Level 3: 37-60 months', 'Level 4: 61-120 months', 'Level 5: 121+ months']
parameter_input_values.append(find_user_input("employer", "Employer", ":office:"))
parameter_input_values.append(find_user_input("citizenship", "citizenship", ":earth_asia:"))
parameter_input_values.append(find_user_input("class_of_admission", "Class of Admission", ":passport_control:"))
parameter_input_values.append(find_user_input("agent_firm", "Agent Firm", ":briefcase:"))
parameter_input_values.append(find_user_input("job_title", "job title", ":necktie:"))
parameter_input_values.append(st.selectbox(':mortar_board:**Select a education level.**', options = education_list))
parameter_input_values.append(st.selectbox(':100:**Select a experience level.**', options = experience_list))
parameter_input_values.append(st.selectbox(':moneybag:**Select a wage level.**', options = wage_level_list))
education_level = parameter_input_values.pop(5)
parameter_input_values.insert(1, education_level)

# Encode user input for prediction
input_variables=pd.DataFrame([parameter_input_values],columns=parameter_list,dtype=object)
for column in input_variables:
    if column in encoders:
        input_variables[column] = encoders[column].transform(input_variables[column])

# Button that triggers the actual prediction
if st.button("***Click Here to Predict you Application Result***"):
    prediction = model.predict(input_variables)
    if prediction == 0:
        st.image(pass_img)
    else:
        st.image(fail_img)