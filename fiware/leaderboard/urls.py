from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^(?P<gameID>[a-zA-Z0-9_\-]+)$', views.GameView.as_view(),
        name="game"),
    url(r'^(?P<gameID>[a-zA-Z0-9_\-]+)/rankedlist$', views.GameRankedListView.as_view(),
        name="game-rankedlist"),
    url(r'^(?P<gameID>[a-zA-Z0-9_\-]+)/(?P<playerID>[a-zA-Z0-9@_\-\.]+)/score$', views.PlayerScoreView.as_view(),
        name="player-score"),
    url(r'^(?P<gameID>[a-zA-Z0-9_\-]+)/(?P<playerID>[a-zA-Z0-9@_\-\.]+)/rankingposition$', views.PlayerRankingView.as_view(),
        name="player-ranking"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
