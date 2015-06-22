import json
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from fiware.ngsi.tests.factories import AccountFactory, OAuth2ApplicationFactory


class GameTests(APITestCase):

    def get_access_token(self, username, password):
        url = reverse("oauth2_provider:token")
        q = {"grant_type": "password",
             "username": username,
             "password": password,
             "client_secret": self.oauth2_client.client_secret,
             "client_id": self.oauth2_client.client_id}
        response = self.client.post(url, q, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)
        return r["access_token"]

    def setUp(self):
        self.user = AccountFactory.create()
        self.oauth2_client = OAuth2ApplicationFactory.create()
        un = getattr(self.user, "username", None) or getattr(self.user, "email", None)
        self.access_token = self.get_access_token(un, "123456")

    def test_put_error(self):
        url = reverse("leaderboard:game", kwargs={"gameID": "testgame"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        data = {}
        response = self.client.put(url, data=data)
        print response.status_code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse("leaderboard:game", kwargs={"gameID": "testgame"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rankedlist(self):
        url = reverse("leaderboard:game-rankedlist", kwargs={"gameID": "testgame"})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_setscore(self):
        url = reverse("leaderboard:player-score", kwargs={"gameID": "testgame", "playerID": self.user.email})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        data = {"scoreEntries": [{"name": "Highscore", "value": 12}]}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getrank(self):
        url = reverse("leaderboard:player-ranking", kwargs={"gameID": "testgame", "playerID": self.user.email})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        data = {"orderBy": "Highscore"}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

