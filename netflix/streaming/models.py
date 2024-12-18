from django.db import models
from django.contrib.auth.models import User
import datetime

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField(default=datetime.date.today)  # Permitir nulos
    poster_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return f"Playlist de {self.user.username}"

class Recommendation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recommendation')
    recommended_movies = models.ManyToManyField(Movie, related_name='recommendations')

    def __str__(self):
        return f"Recommendations for {self.user.username}"
    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name