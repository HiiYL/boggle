from rest_framework import serializers


from boggle.games.models import Game


class GameSerializer(serializers.ModelSerializer):
    time_left = serializers.SerializerMethodField()

    def get_time_left(self,  obj):
        return obj.time_left()

    class Meta:
        model = Game
        fields = ('id', 'token', 'duration', 'board', 'time_left')
