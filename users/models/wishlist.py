from django.db import models
from users.models import User
from movie.models import Movie


# Create your models here.


class Wishlist(models.Model):
    created_at = models.DateTimeField(auto_now_add=True),
    updated_at = models.DateTimeField(auto_now=True),
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist'
