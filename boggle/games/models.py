from django.db import models


class Game(models.Model):
    duration = models.IntegerField()
    board = models.CharField(max_length=255)

    auth_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Submission(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
