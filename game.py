from pysickle.team import Team
from pysickle.player import Player
from pysickle.ball import Ball
from pysickle.goal import Goal
from pysickle.frame import Frame


class Game:
    allGames = []

    def __init__(self, replay):
        Game.allGames.append(self)
        self.metadata = replay['Metadata']
        self.version = replay['Version']
        self.levels = replay['Levels']

        self.replayData = replay['Frames']
        self.maxFrameNo = len(self.replayData) - 1

        self.frames = self.get_frames()

        data = self.parse_one()  # get all basic data from networkstream

        # assign all data
        self.teams = data['teams']
        self.players = data['players']
        self.ball = data['ball']
        print('Teams (ids):', [('%s: %s' % (team.teamID, team.colour)) for team in self.teams])
        # print(self.players)
        print('Players:', [('%s: %s' % (player.name, player.ID)) for player in self.players])
        print('Ball:', self.ball)
        newData = self.parse_two()  # parsing for goals requires players to be assigned to game already. could parse in init, but I'd rather not.

        self.goals = newData['goals']
        # self.hits = [] # will be assigned later - information not in replay
        print('Parsed replay successfully')

        print('Total frames: ' + str(self.maxFrameNo))# this is the number of frames
        lengthOfGame = int(self.replayData[self.maxFrameNo]['Time'])
        print ('Length of game: ' + str(lengthOfGame) + 's')

    def get_frames(self):
        frames = []
        lastTimeRemaining = None
        lastIsOvertime = False
        for frameNo in range(self.maxFrameNo):
            try:
                frame_data = self.replayData[frameNo]
            except KeyError:
                # frame doesnt exist.
                frame_data = None

            frame = Frame(frame_data, lastTimeRemaining, lastIsOvertime)
            lastTimeRemaining = frame.timeRemaining
            lastIsOvertime = frame.isOvertime

            # print(frame.timeRemaining, frameNo)
            frames.append(frame)

        return frames

    def parse_one(self):
        # add player and team data
        teamsAndPlayers = self.look_for_players_and_teams()
        teams = teamsAndPlayers['teams']
        players = teamsAndPlayers['players']

        # add ball data
        gameBall = Ball(self)
        print("Added ball data.")
        return {'teams': teams, 'players': players, 'ball': gameBall}

    def parse_two(self):
        goals = self.find_goals()
        Player.add_all_ids(self)
        Player.add_all_positions(self)
        return {'goals': goals}

    def look_for_players_and_teams(self):
        teams = []
        players = []
        # check first 10 frames for teams
        for frameNo in range(10):
            frame_data = self.replayData[frameNo]

            for _id, _props in frame_data['Spawned'].items():
                if _props["Class"] == 'TAGame.Team_Soccar_TA':
                    team = Team(int(_id), _props)
                    teams.append(team)


        # check first 10 frames for players (has to check after teams as players are immediately assiged to their team
        for frameNo in range(self.maxFrameNo):  # for $#@%!ers who join midgame (looking at you nielskoek)
            frame_data = self.replayData[frameNo]

            for _id, _props in frame_data['Updated'].items():
                if 'Engine.PlayerReplicationInfo:PlayerID' in _props:
                    # print('hi')
                    player = Player.find_players(int(_id), _props)
                    if player:
                        players.append(player)
        return {'teams':teams,'players':players}

    def find_goals(self):
        replayData = self.replayData
        goals = []
        for frameNo in range(self.maxFrameNo):
            frame_data = self.replayData[frameNo]
            for _id, _props in frame_data['Updated'].items():
                if 'TAGame.PRI_TA:MatchGoals' in _props:
                    goal = Goal.add_goals(self, frameNo, int(_id), _props)
                    goals.append(goal)
        # for frameNo in range(self.maxFrameNo):
        #     try:
        #         for actor in replayData[frameNo].actors:
        #             if 'e_Default_' in actor: #prelim check
        #                 actorData = (actor,replayData[frameNo].actors[actor])
        #                 goal = Goal.add_goals(actorData,frameNo,self)
        #                 if goal: goals.append(goal)
        #     except KeyError:
        #         pass #frame just probably doesn't exist
        return goals
    # def analyse(self): #i've tried to keep all interpreting of data here
        # if self.getHitMethod == 2:
            # self.hits = Hit.add_all_hits(self)
        # elif self.getHitMethod == 1:
            # self.hits = Hit._add_all_hits(self)
        # else:
            # print('Unknown hit detection method. Using v2.')
            # self.hits = Hit.add_all_hits(self)

        # self.get_firstHit()

        # replayData = self.replayData
        # print('Total frames: ' + str(self.maxFrameNo))# this is the number of frames
        # lengthOfGame = int(list(replayData.values())[-1].current)
        # print ('Length of game: ' + str(lengthOfGame) + 's')

        # # print(Team.teams)


        # Player.list_players()
        # # print(Game.allgames[0].ball.positions)



    # def get_firstHit(self):
        # for goalNo in range(len(self.goals)):
            # if goalNo == 0: #get first kickoff
                # startFrameNo = 0
            # else:
                # startFrameNo = (self.goals[goalNo-1].frameNo)

            # hitFrameNo = self.maxFrameNo
            # for hit in self.hits:
                # if startFrameNo < hit.frameNo < hitFrameNo:
                    # hitFrameNo = hit.frameNo
            # self.goals[goalNo].firstHit = hitFrameNo

    @classmethod
    def reset_all(cls):
        Team.reset()
        Player.reset()
        Ball.reset()
        Goal.reset()
        # frame doesnt need reset for now
        cls.allGames = []


    def return_structure():
        pass
                # STRUCTURE
# game
    # frames []

    # teams []
        # teamID
        # typeName
        # colour
        # players []
            # team
            # carIDs {frameNo:ID}
            # positions []
            # velocities {frameNo:velocity}
            # properties
            # hits []
    # players []
    # ball
        # positions []
        # velocities {}
        # game
    # goals
        # player
        # frameNo
        # firstHit
    # hits
        # frameNo
        # player
        # velocity
        # position      (ball)
        # carPosition
        # distance
