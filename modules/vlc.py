from windows import player


class Play(player.Player):

    file = None

    def __init__(self, file='tmp/default.mkv'):
        super().__init__(file)
        
        self.file = file

