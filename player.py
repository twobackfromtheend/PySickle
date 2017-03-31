from pysickle.item import Item
from pysickle.team import Team

class Player(Item):
    playerCount = 0
    players = {}  # dictionary of players{id:self}
    allPlayers = []  # list of players as objects
    spectators = {}  # dictionary of spectators {id:self}
    temp = {}

    def __init__(self, name, playerID, uniqueID, gameID, properties, team):
        self.name = name
        self.properties = properties
        self.team = team
        self.ID = int(playerID)
        self.uniqueID = int(uniqueID)
        self.gameID = gameID
        self.carIDs = {}
        self.positions = {}
        self.velocities = {}
        self.rotations = {}
        Player.playerCount += 1
        if team is None:
            Player.temp[playerID] = self
        elif team == 'spectators':
            Player.spectators[playerID] = self
        elif (team.colour == 'orange') or (team.colour == 'blue'):
            self.colour = team.colour
            Player.players[playerID] = self
            Player.allPlayers.append(self)

    @classmethod
    def list_players(cls):
        print('Found players: ')
        playerSerial = 0
        for x in cls.allPlayers:
            print(cls.allPlayers[playerSerial].name + ' on ' + cls.allPlayers[playerSerial].colour + ' team.')
            playerSerial += 1
        # for x in cls.players:
            # print(str(x) + ' is ' + cls.players[x].name)

    @classmethod
    def find_players(cls, _id, _props):
        if 'Engine.PlayerReplicationInfo:bWaitingPlayer' in _props:
            player = cls.assign_waiting_player(_id, _props)
            return player
        elif 'Engine.PlayerReplicationInfo:PlayerName' in _props:
            print('Found Player: %s (id: %s)' % (_props['Engine.PlayerReplicationInfo:PlayerName']['Value'], _id))
            player = cls.add_players(_id, _props)
            return player
        # check for existing spectator that becomes a player.
        elif 'Engine.PlayerReplicationInfo:Team' in _props:
            player = cls.add_existing_spectator(_id, _props)
            return player

        return False

    @classmethod
    def add_players(cls, _id, _props):
        playerName = _props['Engine.PlayerReplicationInfo:PlayerName']['Value']
        playerID = _id
        gameID = int(_props['Engine.PlayerReplicationInfo:PlayerID']['Value'])
        uniqueID = int(_props['Engine.PlayerReplicationInfo:UniqueId']['Value']['Remote']['Value'])
        # check if spectator
        if 'Engine.PlayerReplicationInfo:bIsSpectator' in list(_props.keys()):
            if _props['Engine.PlayerReplicationInfo:bIsSpectator']['Value']:
                print('    ... He is a damn spectator')
                playerTeam = 'spectators'
            else:
                print('why do you have a \'bIsSpectator\' if you are not spectating?')
        else:
            try:
                playerTeamID = int(_props['Engine.PlayerReplicationInfo:Team']['Value']['Int'])  # this is the actor id of the team object ("Archetypes.Teams.Teamx" not x.) (and is flagged data)
                # print(type(playerTeamID))
                # print(type(list(Team.teams.keys())[0]))
                playerTeam = Team.teams[playerTeamID]

            except KeyError:
                print('Cannot find team player belongs to. Adding without team first.')
                # print(list(_props.keys()))
                playerTeam = None
        # print ('playerTeam: ' + str(playerTeam))
        player = cls.create_player(playerName, playerID, uniqueID, gameID, _props, playerTeam)
        if player:
            return player
        return False

    @classmethod
    def create_player(cls, name, playerID, uniqueID, gameID, properties, team):
        for player in list(cls.players.values()):
            if player.uniqueID == uniqueID:
                print('%s has rejoined.' % name)
                cls.players[playerID] = player
                return  # skip the rest, do not readd player.

        if team is None:
            player = cls(name, playerID, uniqueID, gameID, properties, team)
            return player
        elif team == 'spectators':
            cls(name, playerID, uniqueID, gameID, properties, team)
        elif (team.colour == 'orange') or (team.colour == 'blue'):
            player = cls(name, playerID, uniqueID, gameID, properties, team)
            team.players.append(player)
            return player

        return False

    @classmethod
    def add_existing_spectator(cls, _id, _props):
        playerID = _id
        playerTeamID = int(_props['Engine.PlayerReplicationInfo:Team']['Value']['Int'])
        if playerID in cls.spectators:
            player = cls.spectators[playerID]
            print('Spectator joined the match: %s' % player.name)
        elif playerID in cls.temp:
            player = cls.temp[playerID]
            print('Found team info for %s' % player.name)

        # set new values
        player.team = Team.teams[playerTeamID]
        player.team.players.append(player)

        player.colour = player.team.colour
        cls.players[playerID] = player
        cls.allPlayers.append(player)
        return player

    @classmethod
    def assign_waiting_player(cls, _id, _props):
        if _props['Engine.PlayerReplicationInfo:bWaitingPlayer']['Value']:
            print('Found Player: ' + _props['Engine.PlayerReplicationInfo:PlayerName']['Value'])

            playerProperties = _props
            playerName = _props['Engine.PlayerReplicationInfo:PlayerName']['Value']
            playerID = _id
            uniqueID = int(_props['Engine.PlayerReplicationInfo:UniqueId']['Value']['Remote']['Value'])
            gameID = int(_props['Engine.PlayerReplicationInfo:PlayerID']['Value'])

            print('    Has not joined game. Adding info now, assigning to team later.')
            playerTeam = None

            player = cls.create_player(playerName, playerID, uniqueID, gameID, playerProperties, playerTeam)
            return player
        else:
            playerID = _id
            player = cls.temp[playerID]
            try:
                if _props['Engine.PlayerReplicationInfo:bIsSpectator']['Value']:
                    playerTeam = 'spectators'
                    cls.spectators[playerID] = player
                    print('Found Information for: %s (Spectator).' % player.name)

                    del cls.temp[playerID]
            except KeyError:
                pass
            try:
                playerTeamID = int(_props['Engine.PlayerReplicationInfo:Team']['Value']['Int'])
                playerTeam = Team.teams[playerTeamID]
                player.team = playerTeam
                player.team.players.append(player)
                cls.players[playerID] = player
                cls.allPlayers.append(player)
                print('Found Information for: %s (%s).' % (player.name, player.team.colour.title()))

                del cls.temp[playerID]
                return player
            except KeyError:
                pass

    @classmethod
    def add_all_ids(cls, game):
        # actor id for car changes throughout the game (keyframes, goals, demos)
        for frameNo in range(game.maxFrameNo):
            frame_data = game.replayData[frameNo]
            for _id, _props in frame_data['Updated'].items():
                if 'Engine.Pawn:PlayerReplicationInfo' in _props:
                    playerID = int(_props['Engine.Pawn:PlayerReplicationInfo']['Value']['Int'])
                    carID = int(_id)
                    # print('found car for ' + str(playerID))
                    # print([(player, cls.players[player].name) for player in cls.players])
                    # print(cls.players[playerID].carIDs)
                    cls.players[playerID].carIDs[frameNo] = carID
            # try:
            #     for actor in replayData[frameNo].actors:
            #         actorData = (actor,replayData[frameNo].actors[actor])
            #         cls.add_car_ids(actorData,frameNo)
            # except KeyError:
            #     pass #frame just probably doesn't exist

        print('Found %s players.' % len(game.players))
        for player in game.players:
            # print(player.name)
            # complete dict (for missing frames), change to list
            lastCarID = None
            for frameNo in range(game.maxFrameNo):
                if frameNo not in player.carIDs:
                    player.carIDs[frameNo] = lastCarID
                else:
                    lastCarID = player.carIDs[frameNo]
            # print(player.name, player.carIDs[100])

    @classmethod
    def add_all_positions(cls, game):
        for frameNo in range(game.maxFrameNo):
            frame_data = game.replayData[frameNo]

            _ids = list(int(x) for x in frame_data['Updated'].keys())

            for player in game.players:
                carID = player.carIDs[frameNo]
                if carID in _ids:
                    # print(frame_data['Updated'][str(carID)]['TAGame.RBActor_TA:ReplicatedRBState']['Value'])
                    try:
                        position = frame_data['Updated'][str(carID)]['TAGame.RBActor_TA:ReplicatedRBState']['Value']['Position']
                        player.positions[frameNo] = position
                    except KeyError:
                        # print('skjskldklsd', frameNo)
                        pass
                    try:
                        velocity = frame_data['Updated'][str(carID)]['TAGame.RBActor_TA:ReplicatedRBState']['Value']['Velocity']
                        player.velocities[frameNo] = velocity
                    except KeyError:
                        # print('vskjskldklsd', frameNo)
                        pass
                    try:
                        rotation = frame_data['Updated'][str(carID)]['TAGame.RBActor_TA:ReplicatedRBState']['Value']['Rotation']
                        player.rotations[frameNo] = rotation
                    except KeyError:
                        # print('rskjskldklsd', frameNo)
                        pass



        # replayData = game.replayData
        # for frameNo in range(game.maxFrameNo):
        #     try:
        #         for actor in replayData[frameNo].actors:
        #         #for all actors in all frames
        #             actorData = (actor,replayData[frameNo].actors[actor])
        #             if "e_Car_Default" in actor:
        #             # usually _e_Car is enough, but if someone tries to accelerate while counting down (game not started), it won't give position
        #                 if 'TAGame.RBActor_TA:ReplicatedRBState' in actorData[1]['data']:
        #                     cls.add_car_position(actorData,frameNo,game)
        #     except KeyError:
        #         pass #frame just probably doesn't exist

        for player in game.players:
            # complete dict (for missing frames), change to list
            lastCarPosition = (None, None, None)
            # print(player.positions)
            for frameNo in range(game.maxFrameNo):
                if frameNo not in player.positions:
                    player.positions[frameNo] = lastCarPosition
                else:
                    lastCarPosition = player.positions[frameNo]
            # print(player.positions[100], player.name)
        # print(Player.allPlayers[0].carIDs)
            positionList = []
            for frameNo in range(len(player.positions)):
                positionList.append(player.positions[frameNo])
            player.positions = positionList

    @classmethod
    def add_car_position(cls,actorData,frameNo,game):
        actorID = actorData[1]['actor_id']
        for player in game.players: #find player car belongs to
            if player.carIDs[frameNo] == actorID: break
        else:
            # rule out demolition
            if "TAGame.Car_TA:ReplicatedDemolish" in actorData[1]['data']: return

            if frameNo > 100:
                print('Car with no player')
                print('Frame: '+str(frameNo) + ', Car Actor ID: '+str(actorID))

                for player in game.players:
                    print(player.name+', Player ID: '+str(player.ID))
                    print('    Car ID this frame: '+str(player.carIDs[frameNo]))

        position = cls.get_position(actorData)
        if position:
            player.positions[frameNo] = position
        velocity = cls.get_velocity(actorData)
        if velocity:
            player.velocities[frameNo] = velocity
        # else:
            # try:
                # player.velocities[frameNo] = player.velocities[frameNo-1]
                # # print('patching')
            # except UnboundLocalError:
                # pass
        rotation = cls.get_rotation(actorData)
        if rotation:
            player.rotations[frameNo] = rotation
        # else: print('frame: '+str(frameNo) + ', id: '+str(actorID))
        # print('found car for ' + str(playerID))

    @classmethod
    def reset(cls):
        cls.playerCount = 0
        cls.players = {}
        cls.allPlayers = []
        cls.spectators = {}
        cls.temp = {}
