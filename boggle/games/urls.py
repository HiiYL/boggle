from django.urls import register_converter, path
from boggle.games.converters import NegativeIntConverter
from . import views

app_name = 'games'

register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path('', views.GamesView.as_view(), name='games'),
    path('/<negint:game_id>', views.GameDetailView.as_view(), name='get_game'),
]
