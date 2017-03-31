class Goal:
    allGoals = []

    def __init__(self, player, frameNo):
        self.player = player
        self.frameNo = frameNo
        self.firstHit = None  # first hit at kickoff before goal.

    @classmethod
    def add_goals(cls, game, frameNo, _id, _props):
        goalscorer = None
        for player in game.players:
            if _id == player.ID:
                # print(player.name)
                goalscorer = player
                break
        if goalscorer:
            print('Found goal by %s on frame %s' % (goalscorer.name, frameNo))
            goal = Goal(goalscorer, frameNo)
            return goal
        else:
            print('Cannot find goalscorer.')
            print(_id)
            for player in game.players:
                print('%s: %s' % (player.name, player.ID))
            return False
        return goal

    @classmethod
    def reset(cls):
        cls.allGoals = []
