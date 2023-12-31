from movie.views import CommentCreateAPIView
from django.urls import path
from movie import views

app_name = 'movie'

urlpatterns = [

    # Movie
    path('', views.MovieListAPIView.as_view(), name='movie_list'),
    path('similar/<slug:slug>', views.SimilarMovieListAPIView.as_view(), name='movie_similar'),
    path('detail/<slug:slug>', views.MovieRetrieveAPIView.as_view(), name='movie_detail'),

    # Catalog
    path('catalog', views.GenreListAPIView.as_view(), name='catalog_list'),

    # Reviews
    path('review', views.ReviewCreateAPIView.as_view(), name='review_add'),
    path('review/<slug:slug>', views.ReviewListAPIView.as_view(), name='review_list'),
]

# Comment view for url
urlpatterns += [
    path('comments', CommentCreateAPIView.as_view(), name='comment_create'),
    path('comments/like', views.LikeDislikeView.as_view(), name='com'),
    path('comments/<int:movie_id>', views.CommentListAPIView.as_view(), name='movie_comment_list'),
]
