#importing all required libraries
import streamlit as st
import pickle
import pandas as pd
import requests

#set background as wide mode.
st.set_page_config(layout="wide")

#fetching image from API for movies.
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=dceacb26016908d9ff841730298653f9'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/original" + data['poster_path']

#getting 4 recommanded movie using .
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_pos = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_pos.append(fetch_poster(movie_id))
    return recommend_movies, recommend_pos

st.title('Movie Recommender System')
#opening movies file .
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

#opening similarity file of movies.
similarity = pickle.load(open('similarty.pkl', 'rb'))

#providing user list of avilable movies for slecte movie so that movies shoulde be recommanded for him/her.
option = st.selectbox(
    'give your choice',
    movies['title'].values)

# printing trending movies
st.subheader('Trending movies')
uy = st.columns(6)
trends = movies
for i in range(5):
    with uy[i]:
        st.text(trends['title'][i])
        st.image(fetch_poster(trends['id'][i]))
st.subheader("Recommended Movie For You")

#printing the recommanded movies for the user
if option:
    uy = st.columns(6)
    names, poster = recommend(option)
    pickle.dump(names, open('names', 'wb'))
    pickle.dump(poster, open('poster', 'wb'))
    for i in range(5):
        # col=st.columns[i]
        with uy[i]:
            st.text(names[i])
            st.image(poster[i])
