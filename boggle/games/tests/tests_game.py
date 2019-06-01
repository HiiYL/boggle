import json

from django.test import TestCase, Client
from django.urls import reverse

from boggle.games.models import Game
from boggle.games.utils import (
    get_token,
    load_test_board,
)


class GameTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_create_game(self):
        url = reverse('games_api:games')
        duration = 100
        #  test invalid if random is missing
        resp = self.c.post(
            url,
            json.dumps({
                "duration": duration,
            }),
            content_type="application/json"
        )
        self.assertEquals(400, resp.status_code)

        resp = self.c.post(
            url,
            json.dumps({
                "duration": duration,
                "random": False,
                "board": "A,B,C,D"
            }),
            content_type="application/json"
        )
        self.assertEquals(400, resp.status_code)

        resp = self.c.post(
            url,
            json.dumps({
                "duration": duration,
                "random": False,
                "board": "TT, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D"
            }),
            content_type="application/json"
        )
        self.assertEquals(400, resp.status_code)

        resp = self.c.post(
            url,
            json.dumps({
                "duration": duration,
                "random": False,
                "board": "T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D"
            }),
            content_type="application/json"
        )
        self.assertEquals(201, resp.status_code)

        resp = self.c.post(
            url,
            json.dumps({
                "duration": duration,
                "random": False
            }),
            content_type="application/json"
        )
        self.assertEquals(201, resp.status_code)
        data = resp.json()
        self.assertEquals(data['duration'], duration)
        created_game = Game.objects.get(id=data['id'])

        self.assertEquals(created_game.id, data['id'])
        self.assertEquals(created_game.duration, duration)




class GameDetailTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.duration = 100
        self.game = Game.objects.create(
            token=get_token(),
            duration=self.duration,
            board=load_test_board()
        )
        self.url = reverse(
            'games_api:get_game',
            kwargs={'game_id': self.game.id})

    def test_get_game(self):
        resp = self.c.get(self.url)

        self.assertEquals(200, resp.status_code)
        data = resp.json()
        self.assertEquals(data['duration'], self.duration)
        self.assertEquals(data['id'], self.game.id)
        self.assertEquals(data['token'], self.game.token)
        self.assertEquals(data['board'], self.game.board)
        self.assertEquals(data['points'], 0)

    def test_play_game(self):
        # test invalid if token is invalid
        resp = self.c.put(
            self.url,
            json.dumps({
                "token": 'ABCASD',
                "word": "tap"
            })
        )
        self.assertEquals(401, resp.status_code)

        # test  invalid if word is missing
        resp = self.c.put(
            self.url,
            json.dumps({
                "token": self.game.token
            })
        )
        self.assertEquals(400, resp.status_code)

        resp = self.c.put(
            self.url,
            json.dumps({
                "random": False,
                "token": self.game.token,
                "word": "tap"
            })
        )
        self.assertEquals(200, resp.status_code)
