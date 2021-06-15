import pygame


IMAGES = {f'{f}-{n}-{d}': pygame.image.load(f'graphics/warriors/{f}/{n}/{d}.png')
          for f in ['demon', 'elf', 'human', 'undead']
          for n in range(1, 8)
          for d in ['left', 'right']}


class Battle:
    def __init__(self, game, battle_map, interface_image, number, player, enemy):
        self.game = game
        self.battle_map = battle_map
        self.interface_image = interface_image
        self.number = number
        self.player = player
        self.enemy = enemy

    def check_armies(self):
        return len(self.game.player.army) > 0, len(self.game.enemy.army) > 0

    def battle_loop(self):
        pygame.mixer.music.load("music/battle_music.ogg")
        pygame.mixer.music.play(-1)
        while self.game.battle_mode:
            self.draw_battle_interface()
            self.draw_armies()
            self.game.check_events()
            if self.game.BACK_KEY:
                self.game.battle_mode = False
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()

    def draw_battle_interface(self):
        # it needs to be changed to proper battle interface (!)
        self.game.display.blit(self.battle_map, (12, 126))
        self.game.display.blit(self.interface_image, (0, 0))
        self.game.draw_text(f'{self.player.name}', 40, 26, 14, text_format='tl')

    def draw_armies(self):
        for i in range(1, 8):
            if i % 2 == 0:
                self.game.display.blit(IMAGES[f'{self.player.fraction.lower()}-{i}-right'], (128, 710 - (i - 1)*80))
                self.game.display.blit(IMAGES[f'{self.enemy.fraction.lower()}-{i}-left'], (892, 710 - (i - 1)*80))
            else:
                self.game.display.blit(IMAGES[f'{self.player.fraction.lower()}-{i}-right'], (80, 710 - (i - 1)*80))
                self.game.display.blit(IMAGES[f'{self.enemy.fraction.lower()}-{i}-left'], (940, 710 - (i - 1)*80))
