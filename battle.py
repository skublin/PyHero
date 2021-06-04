
class Battle:
    def __init__(self, game, number, player, enemy):
        self.game = game
        self.number = number
        self.player = player
        self.enemy = enemy

    def check_armies(self):
        player = self.player.army
