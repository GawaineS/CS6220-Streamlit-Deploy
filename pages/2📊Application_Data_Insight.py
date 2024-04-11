import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

st.title('PERM Application Data Visualization')
df = joblib.load('./data/dataframe.joblib')

features_1 = ["Employer", "Citizenship", "Class of Admission", "Agent Firm" , "Job Title"]
columns_1 = ["employer", "citizenship", "class_of_admission", "agent_firm" , "job_title"]
features_2 = ["Education Level", "Experience Level", "Wage Level"]
columns_2 = ["education_level", "experience_level" , "wage_level" ]
certified_cases = df[df['case_status'] == 'Certified']
denied_cases = df[df['case_status'] == 'Denied']

def draw_graph_title(title):
    st.markdown("### " + title)
    st.pyplot(plt)

def draw_bar_chart(xlabel, title, data, color):
    plt.figure(figsize=(10, 8))
    data.head(10).plot(kind='barh', color=color)
    plt.xlabel(xlabel)
    plt.ylabel("")
    plt.gca().invert_yaxis()
    draw_graph_title(title)

def draw_top(title, column, df, xlabel, color):
    df_filtered = df[df[column] != 'Others']
    count = df_filtered[column].value_counts().head(10)
    draw_bar_chart(xlabel, title, count, color)

def draw_rate(title, column):
    total = df[column].value_counts()
    certified = certified_cases[column].value_counts()
    total = total[total > 10]
    certified = certified.reindex(total.index, fill_value=0)
    rate = (certified / total).sort_values()
    draw_bar_chart("Certification Rate", title, rate, "lightblue")
    
def draw_distribution(title, column):
    data = certified_cases[column].value_counts()
    plt.figure(figsize=(8, 8))
    data.plot(kind='pie', autopct='%1.1f%%', startangle=160)
    plt.ylabel('')
    draw_graph_title(title)

def load_options(file):
    with open('./data/' + file + '.txt', 'r') as file:
        options = file.readlines()
        options = [option.strip() for option in options]
    return options

def write_result(column, selection):
    st.markdown("### Your Choice of " + selection)
    options = load_options(column)
    choice = st.selectbox("**Select your " + selection + ".**", options)
    certified = len(certified_cases[certified_cases[column] == choice])
    denied = len(denied_cases[denied_cases[column] == choice])
    st.markdown("### Number of Certified Cases: " + str(certified))
    st.markdown("### Number of Denied Cases: " + str(denied))
    st.markdown("### Certificate Rate: " + str(100.0 * certified / (denied + certified)) + "%")

selection = st.sidebar.radio("Select a Feature for Visualization", features_1 + features_2)

if selection in features_1:
    column = columns_1[features_1.index(selection)]
    draw_top("Top 10 " + selection + " by Number of Certified Cases", column, certified_cases, "Number of Certified Applications", "orange")
    draw_top("Top 10 " + selection + " by Number of Denied Cases", column, denied_cases, "Number of Denied Applications", '#1f77b4')
    draw_rate("Bottom 10 " + selection + " by Cerfication Rate", column)
    write_result(column, selection)
else:
    column = columns_2[features_2.index(selection)]
    draw_distribution("Percentage of Certified Applications by " + selection, column)
    draw_rate("Certified Rate Rank", column)
    write_result(column)

