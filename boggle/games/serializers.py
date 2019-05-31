from rest_framework import serializers

from boggle.games.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'token', 'duration', 'board')
