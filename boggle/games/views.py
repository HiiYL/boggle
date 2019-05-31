import json
import binascii
import os

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from boggle.games.models import Game
from boggle.games.serializers import GameSerializer
from boggle.games.utils import (
    is_word_in_dictionary,
    is_word_valid,
    load_test_board,
    load_game_state,
)


class GamesView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        duration = body.get('duration')
        random = body.get('random') == 'true'
        board = body.get('board')

        if random:
            pass  # TODO(hii): implement this
        else:
            if not board:
                board = load_test_board()

        token = binascii.b2a_hex(os.urandom(15)).decode('utf-8')

        game = Game.objects.create(
            board=board,
            duration=duration,
            token=token
        )
        serializer = GameSerializer(game)

        return Response(serializer.data)


class GameDetailView(APIView):
    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def put(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)

        body = json.loads(request.body)
        token = body.get('token')
        word = body.get('word').upper()

        if not token or not word:
            return 'auth token and word required', 400

        if not is_word_in_dictionary(word):
            return 'word is not in dictionary', 400

        if token != game.token:
            return Response(status=401)

        if game.is_expired():
            return Response(status=400)

        game_state = load_game_state(game.board)
        is_valid = is_word_valid(game_state, word)

        if not is_valid:
            return Response(status=401)

        return Response(
            {
                "id": game.id,
                "token": game.token,
                "duration": game.duration,
                "board": game.board,
                "time_left": 10000,
                "points": 10
            }
        )
