import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import numpy as np

projects_df = pd.read_csv('Active_Projects_Under_Construction.csv')
incidents_df = pd.read_csv('Construction-Related_Incidents.csv')

st.title('NYC Construction Projects and Incidents Dashboard')

sidebar_option = st.sidebar.radio('Select View', ('Dashboard', 'Map'))

if sidebar_option == 'Dashboard':
    st.subheader('Dashboard Visualizations')

    plt.figure(figsize=(10, 6))
    sns.countplot(data=projects_df, x='Project type', palette='viridis')
    plt.title('Distribution of Project Types')
    plt.xticks(rotation=45)
    st.pyplot()

    avg_award = projects_df.groupby('Project type')['Construction Award'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_award, x='Project type', y='Construction Award', palette='Blues')
    plt.title('Average Construction Award by Project Type')
    plt.xticks(rotation=45)
    st.pyplot()

    incidents_by_borough = incidents_df.groupby('Borough').size().reset_index(name='Incident Count')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=incidents_by_borough, x='Borough', y='Incident Count', palette='coolwarm')
    plt.title('Incident Count by Borough')
    plt.xticks(rotation=45)
    st.pyplot()

    projects_by_district = projects_df.groupby('Geographical District').size().reset_index(name='Project Count')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=projects_by_district, x='Geographical District', y='Project Count', palette='rocket')
    plt.title('Projects by Geographical District')
    plt.xticks(rotation=45)
    st.pyplot()

    incidents_df['Incident Date'] = pd.to_datetime(incidents_df['Incident Date'])
    incidents_over_time = incidents_df.groupby(incidents_df['Incident Date'].dt.to_period('M')).size()
    plt.figure(figsize=(10, 6))
    incidents_over_time.plot(kind='line', color='orange')
    plt.title('Incidents Over Time')
    plt.ylabel('Number of Incidents')
    st.pyplot()

elif sidebar_option == 'Map':
    st.subheader('Map Visualizations')

    map_option = st.selectbox('Select Map Type', ['Projects Map', 'Incidents Map'])

    if map_option == 'Projects Map':
        st.write("Map of Projects")
        projects_map = folium.Map(location=[40.723072, -73.913267], zoom_start=12)
      
      for _, row in projects_df.iterrows():
            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=row['Project Description'],
                ).add_to(projects_map)

        st.components.v1.html(projects_map._repr_html_(), height=600)

    elif map_option == 'Incidents Map':
        st.write("Map of Incidents")
        incidents_map = folium.Map(location=[40.731121, -73.951061], zoom_start=12)

        for _, row in incidents_df.iterrows():
            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"Accident ID: {row['Accident Report ID']}, Fatality: {row['Fatality']}, Injury: {row['Injury']}",
                ).add_to(incidents_map)

        st.components.v1.html(incidents_map._repr_html_(), height=600)
