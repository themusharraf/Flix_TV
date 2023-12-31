from django.core.validators import FileExtensionValidator
from django_countries.fields import CountryField
from django.db.models import Sum
from django.db import models

from shared.models import BaseModel, upload_name
from movie.models import Genre
from users.models import User


class ActivationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).all()


class Movie(BaseModel):
    class TypeChoice(models.TextChoices):
        movie = "movie", "movie"
        live = "live", "live"
        series = "series", "series"

    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.IntegerField(default=2000)
    film_time_duration = models.IntegerField(default=200)
    age_limit = models.IntegerField(default=20)
    country = CountryField()
    banner = models.ImageField(upload_to=upload_name, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_name, null=True, blank=True)
    type = models.CharField(max_length=255, choices=TypeChoice.choices, default=TypeChoice.movie)
    video_url = models.URLField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    views = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    genre = models.ManyToManyField(Genre)

    class Meta:
        db_table = 'movie'

    def __str__(self):
        return self.title

    @property
    def comments(self):
        return self.comment_set.all()

    @property
    def reviews(self):
        return self.review_set.all()

    @staticmethod
    def count_reviews(movies):  # +++
        return sum(i.reviews.count() for i in movies) or 0

    @staticmethod
    def count_comments(movies):  # +++
        return sum(i.comments.count() for i in movies) or 0

    @staticmethod
    def get_view_sum(movies_added):
        return movies_added.aggregate(total_views=Sum('views'))['total_views'] or 0

    @property
    def get_rate(self):
        if self.review_set.exists():
            return round(sum([review.rating for review in self.review_set.all()]) / self.review_set.count(), 1)
        return 0.0

    @classmethod
    def get_rating(cls, movie):
        if movie.review_set.exists():
            return round(sum([review.rating for review in movie.review_set.all()]) / movie.review_set.count(), 1)
        return 0.0

    @classmethod
    def get_videos(cls, movie):
        return [video.video for video in movie.movievideo_set.all()]

    @classmethod
    def get_genre_list(cls, movie):
        return movie.genre.values_list('title', flat=True)

    @classmethod
    def get_similar_movies(cls, slug):
        try:
            movie = Movie.objects.get(slug=slug)
            movie_genres = movie.genre.all()
            similar_movies = Movie.objects.filter(genre__in=movie_genres).exclude(slug=slug).distinct()

            return similar_movies

        except Movie.DoesNotExist:
            return Movie.objects.none()

    objects = models.Manager()
    active_movies = ActivationManager()


class MovieVideo(models.Model):
    video = models.FileField(upload_to=upload_name,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
                             blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'video'
