from django.db import models
from django.db.models import Manager
from django.utils import timezone


class Game(models.Model):
    duration = models.IntegerField()
    board = models.CharField(max_length=255)

    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def time_left(self):
        seconds_since = int((timezone.now() - self.created_at).total_seconds())
        return max(0, self.duration - seconds_since)

    def is_expired(self):
        return self.time_left() <= 0


class Submission(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
