import requests
from django.conf import settings

def fetch_movies_from_tmdb(endpoint, params=None):
    """Función genérica para interactuar con la API de TMDb."""
    if not params:
        params = {}
    url = f'https://api.themoviedb.org/3/{endpoint}'
    params['api_key'] = settings.TMDB_API_KEY
    params['language'] = 'es-ES'

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error en la API de TMDb: {response.status_code} - {response.text}")
    
def fetch_popular_movies():
    """Obtiene las películas populares desde TMDb."""
    return fetch_movies_from_tmdb('movie/popular')

def fetch_movie_details(movie_id):
    """Obtiene los detalles de una película por su ID."""
    return fetch_movies_from_tmdb(f'movie/{movie_id}')
def fetch_movie_genres():
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': '1fe07a37512a920380b7c85f053ff3ea',
        'language': 'es-ES'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('genres', [])
    return []

def fetch_popular_movies_by_genre():
    """Obtiene las películas populares organizadas por género."""
    genres = fetch_movie_genres()  # Obtén el mapeo de géneros
    data = fetch_movies_from_tmdb('movie/popular')
    movies = data['results']
    
    # Base URL para imágenes
    base_url = "https://image.tmdb.org/t/p/w500/"
    
    # Crear un diccionario para agrupar las películas por género
    movies_by_genre = {genre: [] for genre in genres.values()}
    
    for movie in movies:
        movie['poster_url'] = base_url + movie['poster_path']
        for genre_id in movie['genre_ids']:
            genre_name = genres.get(genre_id, "Otros")
            movies_by_genre[genre_name].append(movie)
    
    return movies_by_genre

def fetch_popular_tv_shows():
    """Obtiene series populares desde la API de TMDB."""
    api_key = '1fe07a37512a920380b7c85f053ff3ea'
    url = f'https://api.themoviedb.org/3/tv/popular'
    params = {
        'api_key': api_key,
        'language': 'es-ES',  # Cambia el idioma si es necesario
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener series populares: {response.status_code}")