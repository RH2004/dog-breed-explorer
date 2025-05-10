# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Page setup
st.set_page_config(page_title="Pawfect Match", page_icon="🐾", layout="wide")
st.title("\U0001f43e Pawfect Match: Explore Dog Breeds")
st.markdown("""
Welcome to **Pawfect Match**, your interactive dog breed explorer! 
Compare traits, explore popularity trends, and find your ideal doggo companion. 🐶💕
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("merged_dog_data.csv")

df = load_data()

# Sidebar image (optional cute dog sticker)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=120)
st.sidebar.header("🐾 Find My Ideal Breed")

# Sidebar filters using correct column names
min_energy = st.sidebar.slider("Minimum Energy", 1, 10, 5)
max_shedding = st.sidebar.slider("Maximum Shedding", 1, 10, 5)
min_friendliness = st.sidebar.slider("Minimum Friendliness", 1, 10, 5)

matches = df[
    ((df['energy_level_value']) >= min_energy/10) &
    ((df['shedding_value']) <= max_shedding/10) &
    ((df['demeanor_value']) >= min_friendliness/10)
]

# Breed selection
st.subheader("🐼 Compare Dog Breeds")
selected_breeds = st.multiselect("Choose breed(s) to compare:", options=df['Breed'].unique())

# Radar chart comparison
if selected_breeds:
    radar_df = df[df['Breed'].isin(selected_breeds)][
        ['Breed', 'demeanor_value', 'energy_level_value', 'shedding_value', 'trainability_value']
    ]
    radar_df.rename(columns={
        'demeanor_value': 'Friendliness',
        'energy_level_value': 'Energy',
        'shedding_value': 'Shedding',
        'trainability_value': 'Trainability'
    }, inplace=True)
    
    fig = go.Figure()
    for _, row in radar_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[1:].values,
            theta=radar_df.columns[1:].tolist(),
            fill='toself',
            name=row['Breed']
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 4])),
        height=600,
        width=800,
        margin=dict(t=40, b=40, l=40, r=40),
        showlegend=True,
        template="plotly_white",
        title="🐕 Trait Comparison Across Selected Breeds"
    )
    st.plotly_chart(fig, use_container_width=False)

# Popularity chart
if st.checkbox("📈 Show Popularity Over Time"):
    year_cols = [col for col in df.columns if col.startswith("Ranking")]
    popularity_df = df[df['Breed'].isin(selected_breeds)] if selected_breeds else df

    melted = popularity_df.melt(
        id_vars='Breed',
        value_vars=year_cols,
        var_name='Year',
        value_name='Ranking'
    )
    melted['Year'] = melted['Year'].str.extract('(\d+)').astype(int)

    fig2 = px.line(
        melted.sort_values('Year'),
        x="Year",
        y="Ranking",
        color="Breed",
        markers=True,
        template="simple_white",
        title="🌟 Breed Popularity Over Time"
    )
    fig2.update_yaxes(autorange="reversed")
    fig2.update_layout(
        height=500,
        width=900,
        margin=dict(t=40, b=40, l=40, r=40)
    )
    st.plotly_chart(fig2, use_container_width=False)

# Ideal breed recommendation
st.subheader("🎯 Recommended Breeds Based on Preferences")
if not matches.empty:
    st.dataframe(matches[['Breed', 'energy_level_value', 'shedding_value', 'demeanor_value', 'trainability_value']].rename(columns={
        'energy_level_value': 'Energy',
        'shedding_value': 'Shedding',
        'demeanor_value': 'Friendliness',
        'trainability_value': 'Trainability'
    }).sort_values(by='Friendliness', ascending=False))
    st.markdown("---")
    st.markdown("© 2025 Reda HEDDAD — Powered by Streamlit")
else:
    st.warning("Oops! No matches found. Try adjusting your filters. 😞")
    st.markdown("---")
    st.markdown("© 2025 Reda HEDDAD — Powered by Streamlit")

