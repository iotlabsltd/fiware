class TestGames(object):

    def __init__(self, game_id):
        self.game_id = game_id

    @classmethod
    def create(self, game_id, highScoreNames=None, maxEntries=None,
               onlyKeepBestEntry=None, socialNetwork=None):
        return True

    @classmethod
    def delete(self, game_id):
        return True

    def getRankedList(self, rankStart=None, rankEnd=None, orderBy=None):
        return [{"playerID": "foo",
                 "rankPosition": 1,
                 "ScoreEntries": [],
                 "userData": {},
                 "imgURL": ""}]

    def setPlayerScore(self, player_id, scoreEntries=None, userData=None):
        # scoreEntries = [{"name": .., "value": ..}, ]
        return True

    def getPlayerRank(self, player_id, orderBy=None):
        return {"playerID": "foo",
                 "rankPosition": 1,
                 "ScoreEntries": [],
                 "userData": {},
                 "imgURL": ""}
