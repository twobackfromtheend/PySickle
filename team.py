# from player import Player

class Team:
    teams = {}  # dictionary of teams (actor id, self)
    allTeams = []  # list of teams as objects

    def __init__(self, _id, _props):
        self.teamID = int(_id)
        self.typeName = _props['Name']

        if self.typeName.endswith('1'):
            self.colour = 'orange'
            print('Found orange (%s)' % _id)
        else:
            self.colour = 'blue'
            print('Found blue (%s)' % _id)
        self.players = []

        Team.teams[self.teamID] = self
        Team.allTeams.append(self)

    @classmethod
    def reset(cls):
        cls.teams = {}
        cls.allTeams = []

    # @classmethod
    # def find_and_add_teams(cls, actorData):
    #     if 'n_Team' in actorData[0]:
    #         # print('hi')
    #         teamID = actorData[1]['actor_id']
    #         typeName = actorData[1]['actor_type']
    #         if typeName.endswith('1'): #50% chance to get this correct, simply means it is wrong.
    #             colour = 'orange'
    #             team = cls(teamID,typeName,colour)
    #             # print('found orange')
    #         else:
    #             colour = 'blue'
    #             team = cls(teamID,typeName,colour)
    #             # print('found blue')
    #         return team
    #     return False

    # @staticmethod
    # def create_player(name,playerID,properties,team):
        # if team == 'spectators':
            # Player(name,playerID,properties,team)
        # else:
            # player = Player(name,playerID,properties,team)
            # team.players.append(player)
            # return player
        # return False
