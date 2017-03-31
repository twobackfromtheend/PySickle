from pysickle.item import Item


class Ball(Item):
    balls = []

    def __init__(self, game):
        self.game = game
        self._ids = self.find_all_ids()
        print(self._ids)
        # print(self._ids)
        self.positions = {}
        self.velocities = {}
        Ball.add_all_positions_and_velocities(self)

        Ball.balls.append(self)

    def find_all_ids(self):
        _ids = []  # [(startframe:id), (s:i) .. ]

        for frameNo in range(self.game.maxFrameNo):
            frame_data = self.game.replayData[frameNo]['Spawned']
            for _id, _props in frame_data.items():
                if _props['Class'] == 'TAGame.Ball_TA':
                    _ids.append((frameNo, int(_id)))
        return _ids

    def add_all_positions_and_velocities(self):
        replayData = self.game.replayData
        _id_index = 0
        _change_at = self._ids[1][0]  # second id frame. second id is [1][1]
        _id = str(self._ids[0][1])

        lastBallPosition = (0, 0, 0)
        for frameNo in range(self.game.maxFrameNo):
            frame_data = replayData[frameNo]

            if frameNo == _change_at:
                # use new id
                _id_index += 1
                _id = str(self._ids[_id_index][1])
                try:
                    _change_at = self._ids[_id_index + 1][0]
                except IndexError:
                    # last change hit
                    pass
                # print('set _id to %s, change at to %s, on frame %s with _id_index %s' % (_id, _change_at, frameNo, _id_index))

            # print(frame_data["Updated"])
            if _id in frame_data["Updated"]:
                try:
                    position = frame_data["Updated"][_id]["TAGame.RBActor_TA:ReplicatedRBState"]["Value"]['Position']
                    # print(position)
                except KeyError:  # no position info
                    position = None
                try:
                    velocity = frame_data["Updated"][_id]["TAGame.RBActor_TA:ReplicatedRBState"]["Value"]['LinearVelocity']
                except KeyError:  # no velocity info
                    velocity = None

                if position:
                    self.positions[frameNo] = position
                if velocity:
                    self.velocities[frameNo] = velocity
        #     try:
        #         for actor in replayData[frameNo].actors:
        #         #for all actors in all frames
        #             actorData = (actor,replayData[frameNo].actors[actor])
        #             if "e_Ball_Default" in actor:
        #                 if 'TAGame.RBActor_TA:ReplicatedRBState' in actorData[1]['data']:
        #                     Ball.add_ball_position(self,actorData,frameNo)
        #     except KeyError:
        #         pass #frame just probably doesn't exist

        #complete dict (for missing frames), change to list
        lastBallPosition = (0,0,0)
        for frameNo in range(self.game.maxFrameNo):
            if frameNo not in self.positions:
                self.positions[frameNo] = lastBallPosition
            else:
                lastBallPosition = self.positions[frameNo]

        # convert to list
        positionList = []
        for frameNo in range(len(self.positions)):
            positionList.append(self.positions[frameNo])
        self.positions = positionList

    def add_ball_position(self,actorData,frameNo):
        position = Ball.get_position(actorData)
        if position:
            self.positions[frameNo] = position
        # get velocity too as it's related, and unworthy of its own function
        velocity = Ball.get_velocity(actorData)
        if velocity:
            self.velocities[frameNo] = velocity

    @classmethod
    def reset(cls):
        cls.balls = []
