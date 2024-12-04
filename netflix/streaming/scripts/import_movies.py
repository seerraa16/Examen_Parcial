import requests
from streaming.models import Movie

API_KEY = "c2dc323ab66e5495c27791ea6469e55e"

def fetch_and_store_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for movie_data in data['results']:
            movie, created = Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'description': movie_data['overview'],
                    'release_date': movie_data.get('release_date', None),
                    'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}",
                    'backdrop_url': f"https://image.tmdb.org/t/p/w500{movie_data['backdrop_path']}",
                }
            )
            if created:
                print(f"Added: {movie.title}")
    else:
        print("Failed to fetch data from TMDb.")