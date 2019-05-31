import json
import binascii
import os

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from boggle.games.models import Game
from boggle.games.serializers import GameSerializer
from boggle.games.utils import load_test_board


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
