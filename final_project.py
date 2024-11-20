import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('career_change_prediction_dataset.csv')

st.set_page_config(page_title="Career Change Prediction", layout="wide")

st.title("Career Change Prediction Dashboard")
st.markdown("Analyze factors influencing career changes with interactive visualizations.")

st.sidebar.header("Filter Data")
gender = st.sidebar.multiselect("Select Gender", options=data['Gender'].unique(), default=data['Gender'].unique())
education = st.sidebar.multiselect("Select Education Level", options=data['Education Level'].unique(), default=data['Education Level'].unique())
field = st.sidebar.multiselect("Select Field of Study", options=data['Field of Study'].unique(), default=data['Field of Study'].unique())

filtered_data = data[(data['Gender'].isin(gender)) & 
                     (data['Education Level'].isin(education)) &
                     (data['Field of Study'].isin(field))]

st.header("Overview of the Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(filtered_data))
col2.metric("Average Age", round(filtered_data['Age'].mean(), 2))
col3.metric("Avg Job Satisfaction", round(filtered_data['Job Satisfaction'].mean(), 2))

st.subheader("Field of Study Distribution")
field_count = filtered_data['Field of Study'].value_counts()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=field_count.values, y=field_count.index, palette="viridis", ax=ax)
ax.set_title("Number of Records by Field of Study")
ax.set_xlabel("Count")
ax.set_ylabel("Field of Study")
st.pyplot(fig)

st.subheader("Age Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_data['Age'], kde=True, bins=20, color="skyblue", ax=ax)
ax.set_title("Age Distribution")
ax.set_xlabel("Age")
ax.set_ylabel("Frequency")
st.pyplot(fig)

st.subheader("Job Security vs Likelihood to Change Occupation")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_data, x="Job Security", y="Likely to Change Occupation", hue="Gender", ax=ax, palette="Set2", alpha=0.6)
ax.set_title("Job Security vs Likelihood to Change Occupation")
ax.set_xlabel("Job Security")
ax.set_ylabel("Likely to Change Occupation (1 = Yes)")
st.pyplot(fig)

st.subheader("Filtered Data")
st.dataframe(filtered_data)