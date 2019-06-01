from django.urls import include, path


urlpatterns = [
    path('games', include('boggle.games.urls', 'games_api')),
]
