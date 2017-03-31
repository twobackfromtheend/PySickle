class Frame:
    # allFrames = {}
    # allFramesList = []

    def __init__(self, frame_data, lastTimeRemaining, lastIsOvertime):
        self.frameNo = frame_data['Number']
        self.time = frame_data['Time']
        self.delta = frame_data['Delta']
        self.is_KeyFrame = bool(frame_data['IsKeyFrame'])
        timeRemaining, isOvertime = self.parse_frame(lastTimeRemaining, frame_data)


        if timeRemaining is None:
            timeRemaining = lastTimeRemaining
        if isOvertime is None:
            isOvertime = lastIsOvertime

        self.timeRemaining = timeRemaining
        self.isOvertime = isOvertime

        # GameFrame.allFramesList.append(self)
        # GameFrame.allFrames[frameNo] = self

    def parse_frame(self, lastTimeRemaining, frame_data):
        timeRemaining = None
        isOvertime = None
        updated = frame_data['Updated']

        for _id, _props in updated.items():
            if 'TAGame.GameEvent_Soccar_TA:SecondsRemaining' in _props:
                timeRemaining = _props['TAGame.GameEvent_Soccar_TA:SecondsRemaining']['Value']
                # print(timeRemaining, type(timeRemaining))
                # print('huh', timeRemaining)
            if 'TAGame.GameEvent_Soccar_TA:bOverTime' in _props:
                isOvertime = _props['TAGame.GameEvent_Soccar_TA:bOverTime']['Value']
                # print('hi', isOvertime)

        return (timeRemaining, isOvertime)


