from django.urls import path
from .views import MovieListView, MovieDetailView, PlaylistView, RecommendationView, home
from .views import popular_movies, movie_details, search_movies
from .views import categories, my_list
from .views import search_movies
from . import views

app_name = 'streaming'


urlpatterns = [
    path('', home, name='home'),
    path('api/popular/', popular_movies, name='popular-movies'),
    path('api/movie/<int:movie_id>/', movie_details, name='movie-details'),
    path('api/movies/', MovieListView.as_view(), name='movie-list'),
    path('api/movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('api/playlists/', PlaylistView.as_view(), name='playlist'),
    path('api/recommendations/', RecommendationView.as_view(), name='recommendation'),
    path('search/', search_movies, name='search-movies'),
    path('categories/', views.categories, name='categories'),  # Mantén esta para la página de categorías
    path('categories/<int:genre_id>/', views.movies_by_category, name='movies-by-category'),  # Mantén esta para los géneros
    path('my-list/', my_list, name='my-list'),
]