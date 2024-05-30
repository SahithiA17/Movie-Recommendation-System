from flask import Flask, render_template, request, url_for
import pickle
import requests

app = Flask(__name__)

# Load the data from pickle files
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].values
    recommended_movie_names = []
    recommended_movie_posters = []

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    return render_template('index.html', movie_list=movie_list, recommended_movie_names=recommended_movie_names, recommended_movie_posters=recommended_movie_posters)

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
