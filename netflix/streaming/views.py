from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer
from django.http import JsonResponse
from .utils import fetch_popular_movies, fetch_movie_details
from django.shortcuts import render, get_object_or_404
from .models import Genre


# Vista Home para plantillas
# Vista Home para plantillas
def home(request):
    """Obtiene películas populares y las muestra en la plantilla de inicio."""
    try:
        data = fetch_popular_movies()  # Llama a la función que obtiene películas populares
        movies = data['results']  # La clave 'results' contiene las películas
        # Añadir la base de URL para las imágenes
        base_url = "https://image.tmdb.org/t/p/w500/"
        for movie in movies:
            movie['poster_url'] = base_url + movie['poster_path']
        return render(request, 'home.html', {'movies': movies})  # Enviar películas a la plantilla
    except Exception as e:
        return render(request, 'home.html', {'error': str(e)})


from django.shortcuts import render

def categories(request):
    return render(request, 'categories.html')

def my_list(request):
    return render(request, 'my_list.html')




from django.shortcuts import render
from .utils import fetch_movies_from_tmdb

# Vista de búsqueda
def search_movies(request):
    query = request.GET.get('query', '')
    movies = []

    if query:
        api_key = '1fe07a37512a920380b7c85f053ff3ea'  # O usa settings.TMDB_API_KEY si lo defines en settings.py
        url = f'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': api_key,
            'query': query,
            'language': 'es-ES'  # Cambia el idioma si es necesario
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])

    return render(request, 'search_results.html', {'movies': movies, 'query': query})

# Vistas para la API
import requests
from django.shortcuts import render

# API Key
API_KEY = '1fe07a37512a920380b7c85f053ff3ea'

# Vista para mostrar categorías
def categories(request):
    url = f'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': API_KEY,
        'language': 'es-ES'  # Cambia el idioma si es necesario
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        genres = data.get('genres', [])
    else:
        genres = []

    return render(request, 'categories.html', {'genres': genres})




from django.shortcuts import render, get_object_or_404
from .models import Genre
from .models import Movie  # Assuming Movie model exists

def movies_by_category(request, genre_id):
    # Get the genre, or return 404 if not found
    genre = get_object_or_404(Genre, id=genre_id)
    
    # Query movies based on the genre
    movies = Movie.objects.filter(genre=genre)
    
    return render(request, 'movies_by_category.html', {'genre': genre, 'movies': movies})



class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

class PlaylistView(APIView):
    def get(self, request):
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        playlist = Playlist.objects.create(name=data['name'], user=request.user)
        if 'movies' in data:
            for movie_id in data['movies']:
                movie = Movie.objects.get(id=movie_id)
                playlist.movies.add(movie)
        playlist.save()
        return Response(PlaylistSerializer(playlist).data, status=status.HTTP_201_CREATED)

class RecommendationView(APIView):
    def get(self, request):
        try:
            recommendation = Recommendation.objects.get(user=request.user)
            serializer = RecommendationSerializer(recommendation)
            return Response(serializer.data)
        except Recommendation.DoesNotExist:
            return Response({"message": "No recommendations found."}, status=status.HTTP_404_NOT_FOUND)



def popular_movies(request):
    """Vista para obtener películas populares."""
    try:
        data = fetch_popular_movies()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def movie_details(request, movie_id):
    """Vista para obtener detalles de una película."""
    try:
        data = fetch_movie_details(movie_id)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)