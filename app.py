import streamlit as st
import pickle
import pandas as pd
import requests
import bz2 as bz2



def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0MTZhZGI1OTBhZmZiNzNjMjRiMDQ0ZjM2M2JkZWI3MCIsInN1YiI6IjY0ZTljOGEzOTBlYTRiMDBlNDlkZmQ3MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.TKlQNklKGHQXe83L141wtTWE3betHOcWZek5bErv3QM"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    #print(data)
   # print(response.text)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies= []
    recommended_poster = []
    for i in movies_list:
        # print(i[0]) #it returns indexes
        movie_id= movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))
    return recommended_movies , recommended_poster


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies= pd.DataFrame(movies_dict)
def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as f:
        data = pickle.load(f)
    return data



similarity = decompress_pickle('similarity.pbz2')


#similarity=pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Enter the name of the movie you watched',movies['title'].values)

if st.button('Recommend'):
  names,posters =  recommend(selected_movie_name)
  col1, col2, col3, col4, col5= st.columns(5)

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
  #for i in recommendations:
       # st.write(i)


