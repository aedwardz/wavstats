from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home_page"),
    path("env/<str:pssword>", views.showEnvs, name = ".env"),
    path("favgame/<str:game>/", views.games, name="favorite_game"),
    path("<str:artist>", views.spotifyStats, name="spotify_stats")
]