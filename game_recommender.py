import streamlit as st
import pandas as pd

st.set_page_config(page_title="Game Recommender", layout="centered")
st.title("AI-Powered Recommendation System")
st.subheader("Recommended Games:")

@st.cache_data
def load_data():
    return pd.read_csv("video_game_reviews.csv")[['Game Title', 'User Rating', 'Price', 'Genre']].dropna()

df = load_data()

st.subheader("Filters")
genre_list = ["-- Any Genre --"] + sorted(df['Genre'].dropna().unique())
selected_genre = st.selectbox("Genre:", genre_list)

min_price = float(df["Price"].min())
max_price = float(df["Price"].max())

col1, col2 = st.columns(2)
with col1:
    price_min = st.number_input("Min price", min_value=min_price, max_value=max_price, value=min_price, step=0.5, format="%.2f")
with col2:
    price_max = st.number_input("Max price", min_value=min_price, max_value=max_price, value=max_price, step=0.5, format="%.2f")

def get_recommendations(genre, pmin, pmax):
    filtered = df[(df['Price'] >= pmin) & (df['Price'] <= pmax)]
    if genre != "-- Any Genre --":
        filtered = filtered[filtered['Genre'].str.lower() == genre.lower()]
    return filtered.sort_values(by='User Rating', ascending=False).head(5)

if st.button("Get Recommendations"):
    st.subheader("Recommended Games:")
    results = get_recommendations(selected_genre, price_min, price_max)
    if results.empty:
        st.write("_No recommendations available with the selected filters_")
    else:
        st.dataframe(results.reset_index(drop=True))
