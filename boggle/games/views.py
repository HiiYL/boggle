import json
import binascii
import os

from rest_framework.response import Response
from rest_framework.views import APIView

from boggle.games.models import Game, Submission
from boggle.games.serializers import GameSerializer
from boggle.games.utils import (
    is_word_in_dictionary,
    is_word_valid,
    load_test_board,
    get_random_board,
    load_game_state,
)


class GamesView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        duration = body.get('duration')
        random = body.get('random')
        board = body.get('board')

        if random is None:
            return Response(
                {'message': 'random must be defined'},
                status=400
            )

        if random:
            board = get_random_board()
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

        return Response(serializer.data, status=201)


class GameDetailView(APIView):
    def get(self, request, game_id):
        game = None
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'message': 'game not found'}, status=404)

        serializer = GameSerializer(game)
        return Response(serializer.data)

    def put(self, request, game_id):
        game = None
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'message': 'game not found'}, status=404)

        body = json.loads(request.body)
        token = body.get('token')
        word = body.get('word').upper()

        if not token or not word:
            return Response(
                {'message': 'token and word must both be provided'},
                status=400
            )

        if not is_word_in_dictionary(word):
            return Response(
                {'message': 'word is not a valid dictionary word'},
                status=400
            )

        if token != game.token:
            return Response(
                {'message': 'token is invalid'},
                status=401
            )

        if game.is_expired():
            return Response(
                {'message': 'game has expired'},
                status=400
            )

        game_state = load_game_state(game.board)

        submission = Submission.objects.filter(game=game, word=word)

        if not submission.exists():
            is_valid = is_word_valid(game_state, word)

            if not is_valid:
                return Response(
                    {'message': 'word was not found in the board'},
                    status=400
                )
            submission = Submission.objects.create(
                game=game,
                word=word,
                score=len(word),
            )

        return Response(
            {
                "id": game.id,
                "token": game.token,
                "duration": game.duration,
                "board": game.board,
                "time_left": 10000,
                "points": submission.score,
            }
        )
