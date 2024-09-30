import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('lotr_characters.csv')
df = df.dropna(how='all', axis=1)

st.title("Lord of the Rings: A Nerdy Character Explorer")
st.markdown("""
    Welcome to **Middle-Earth**'s ultimate character exploration tool!
    Explore the rich world of J.R.R. Tolkien's legendarium through the lens of data science.
    Filter through races, realms, and even hairstyles (yes, we have that covered).
    Let's uncover hidden patterns in the data about your favorite characters.
""")

st.sidebar.header("Choose Your Filters")
selected_race = st.sidebar.multiselect("Filter by Race", df["race"].dropna().unique()) if 'race' in df.columns else []
selected_gender = st.sidebar.multiselect("Filter by Gender", df["gender"].dropna().unique()) if 'gender' in df.columns else []
selected_realm = st.sidebar.multiselect("Filter by Realm", df["realm"].dropna().unique()) if 'realm' in df.columns else []

filtered_df = df.copy()
if selected_race: filtered_df = filtered_df[filtered_df["race"].isin(selected_race)]
if selected_gender: filtered_df = filtered_df[filtered_df["gender"].isin(selected_gender)]
if selected_realm: filtered_df = filtered_df[filtered_df["realm"].isin(selected_realm)]

def plot_bar_chart(column_name, title):
    counts = filtered_df[column_name].value_counts().sort_values(ascending=True)
    fig = go.Figure(go.Bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        marker=dict(color='steelblue')
    ))
    fig.update_layout(title=title, xaxis_title="Count", yaxis_title=column_name, height=500)
    return fig

if not filtered_df.empty:
    st.subheader("Descriptive Statistics")
    
    if 'gender' in filtered_df.columns:
        with st.container():
            st.write("### Gender Distribution")
            st.plotly_chart(plot_bar_chart("gender", "Gender Distribution in Middle-Earth"), use_container_width=True)
    
    if 'hair' in filtered_df.columns:
        with st.container():
            st.write("### Hair Distribution")
            st.plotly_chart(plot_bar_chart("hair", "Hair Colors of Middle-Earth"), use_container_width=True)
    
    if 'race' in filtered_df.columns:
        with st.container():
            st.write("### Race Distribution")
            st.plotly_chart(plot_bar_chart("race", "Race Distribution in Middle-Earth"), use_container_width=True)
    
    if 'realm' in filtered_df.columns:
        with st.container():
            st.write("### Realm Distribution")
            st.plotly_chart(plot_bar_chart("realm", "Realms of Middle-Earth"), use_container_width=True)
else:
    st.warning("No data available based on the current filters. It seems the forces of Mordor are obscuring our view.")

st.subheader("Filtered DataFrame")
st.write(filtered_df)

st.markdown("""
    *In the darkness bind them.*
    This app is brought to you by your friendly neighborhood data wizards. 
    May your journey through Middle-Earth be data-driven and full of discovery.
""")
