import streamlit as st # type: ignore
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/search/movie/{}?api_key=89588376dbf6b3ceb37b0ab089ba0b35'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']  # Fix the typo here


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(id))

    return recommended_movies, recommended_movies_posters


# Load movie list and similarity matrix
movies_list = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# App title
st.title('Rectify-Movie Recommender System')

# Movie selection
selected_movie_name = st.selectbox(
    'Search Movies and Many More',
    movies['title'].values)

# Recommend movies when button is clicked
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Use st.columns instead of deprecated st.beta_columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
