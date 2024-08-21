from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home_page"),
    path("env/<str:pssword>", views.showEnvs, name = ".env"),
    path("<str:artist>", views.spotifyStats, name="spotify_stats"),
    path("test/inheritance", views.artistPage, name="artist-page"),
    path("search/<str:artistId>", views.artistPage, name="artist_page")
]