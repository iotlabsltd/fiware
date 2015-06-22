from django.conf import settings

from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from oauth2_provider.ext.rest_framework import OAuth2Authentication

# from django_recycle.utils.loading import import_class

from fiware.utils import import_class

GAMES = getattr(settings, "FIWARE_LEADERBOARD_GAMES", None)


class GameView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]

    def put(self, request, *args, **kwargs):
        game_id = kwargs.get("gameID", None)
        if game_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if GAMES is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        gklass = import_class(GAMES)
        if gklass.create(game_id, **request.data) is True:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, *args, **kwargs):
        game_id = kwargs.get("gameID", None)
        if game_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if GAMES is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        gklass = import_class(GAMES)
        if gklass.delete(game_id) is True:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class GameRankedListView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]

    def get(self, request, *args, **kwargs):
        game_id = kwargs.get("gameID", None)
        if game_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if GAMES is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        gklass = import_class(GAMES)
        game = gklass(game_id)
        l = game.getRankedList(**request.data)
        return Response(data=l, status=status.HTTP_200_OK)


class PlayerScoreView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]

    def post(self, request, *args, **kwargs):
        game_id = kwargs.get("gameID", None)
        if game_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        player_id = kwargs.get("playerID", None)
        if player_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if GAMES is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        gklass = import_class(GAMES)
        game = gklass(game_id)
        game.setPlayerScore(player_id, **request.data)
        return Response(status=status.HTTP_200_OK)


class PlayerRankingView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]

    def get(self, request, *args, **kwargs):
        game_id = kwargs.get("gameID", None)
        if game_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        player_id = kwargs.get("playerID", None)
        if player_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if GAMES is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        gklass = import_class(GAMES)
        game = gklass(game_id)
        r = game.getPlayerRank(player_id, **request.data)
        return Response(data=r,status=status.HTTP_200_OK)


