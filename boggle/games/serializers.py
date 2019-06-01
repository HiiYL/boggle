from django.db.models import Sum
from rest_framework import serializers

from boggle.games.models import Game, Submission


class GameSerializer(serializers.ModelSerializer):
    time_left = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    def get_time_left(self,  obj):
        return obj.time_left()

    def get_points(self, obj):
        return obj.submissions.aggregate(Sum('score'))['score__sum'] or 0

    class Meta:
        model = Game
        fields = ('id', 'token', 'duration', 'board', 'time_left', 'points')
