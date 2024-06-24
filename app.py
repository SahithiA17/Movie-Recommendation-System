from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# Load the data from pickle files (replace with your actual data loading logic)
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

OMDB_API_KEY = 'YOUR_OMDB_API_KEY'

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    poster_path = data.get('Poster', '')
    return poster_path if poster_path != 'N/A' else None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommended_movie_posters.append(fetch_poster(movie_title))
        recommended_movie_names.append(movie_title)

    return recommended_movie_names, recommended_movie_posters

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].values
    recommended_movie_names = []
    recommended_movie_posters = []
    selected_movie = None

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    return render_template('index.html', movie_list=movie_list, recommended_movie_names=recommended_movie_names, recommended_movie_posters=recommended_movie_posters, selected_movie=selected_movie)

if __name__ == '__main__':
    app.run(debug=True)
