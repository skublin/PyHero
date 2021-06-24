import pygame
from structures.graph import Graph
from random import choice


IMAGES = {'settings_prompt': pygame.image.load('graphics/settings_prompt.png'),
          'speed_up': pygame.image.load('graphics/btn/speed_up.png'),
          'speed_down': pygame.image.load('graphics/btn/speed_down.png'),
          'music_up': pygame.image.load('graphics/btn/music_up.png'),
          'music_down': pygame.image.load('graphics/btn/music_down.png'),
          'music_mute': pygame.image.load('graphics/btn/music_mute.png')}


# available positions (195) on world map (Tuple with x and y)
# i - row number, j - position in row number (column number)
class World:
    """
    This class helps in world configuration (graph) and makes settings.
    """
    def __init__(self, game):
        self.game = game
        self.size = len(self.game.POSITIONS[:]), len(self.game.POSITIONS[0][:])
        self.G = Graph()
        self.build_graph()
        self.game_speed = 500
        self.music_volume = 1.0
        self.music_mute = False
        self.buttons = dict()
        self.map_events = {'extra_money': [(1, 4), (1, 9), (1, 13), (2, 3), (3, 8), (5, 6), (5, 11),
                                           (7, 3), (7, 6), (7, 10), (9, 1), (9, 10), (9, 13), (11, 3)],
                           'extra_exp': [(2, 1), (2, 13), (5, 0), (5, 9), (5, 13), (8, 5), (10, 1), (11, 2)],
                           'extra_sp': [(0, 0), (1, 10), (3, 0), (3, 9), (4, 3), (6, 2), (7, 13), (9, 7), (12, 12)],
                           'extra_moves': [(3, 1), (3, 5), (3, 6), (3, 7), (3, 13), (4, 1), (4, 12),
                                           (4, 11), (5, 4), (5, 5), (5, 12), (8, 1), (8, 2), (9, 2),
                                           (9, 6), (10, 5), (10, 9), (10, 10), (11, 6), (11, 7), (11, 9)]}

    # map size: n x m (rows x columns)
    def build_graph(self):
        n, m = self.size
        # first graph G with only vertices (i, j)
        for i in range(n):
            for j in range(m):
                self.G.add_vertex((i, j))
        # next every vertex gets all possible neighbours
        for v in self.G:
            v_i, v_j = v.id
            self.G.add_edge((v_i, v_j), (v_i, v_j), cost=0)
            if v_j + 1 <= 14:
                self.G.add_edge((v_i, v_j), (v_i, v_j + 1))
                if v_i % 2 != 0:
                    if v_i - 1 >= 0:
                        self.G.add_edge((v_i, v_j), (v_i - 1, v_j + 1))
                    if v_i + 1 <= 12:
                        self.G.add_edge((v_i, v_j), (v_i + 1, v_j + 1))
            if v_j - 1 >= 0:
                self.G.add_edge((v_i, v_j), (v_i, v_j - 1))
                if v_i % 2 == 0:
                    if v_i - 1 >= 0:
                        self.G.add_edge((v_i, v_j), (v_i - 1, v_j - 1))
                    if v_i + 1 <= 12:
                        self.G.add_edge((v_i, v_j), (v_i + 1, v_j - 1))
            if v_i + 1 <= 12:
                self.G.add_edge((v_i, v_j), (v_i + 1, v_j))
            if v_i - 1 >= 0:
                self.G.add_edge((v_i, v_j), (v_i - 1, v_j))

    def change_speed(self, up_down):
        if self.game_speed == 500:
            if up_down == 'up':
                # slow speed
                self.game_speed = 250
            elif up_down == 'down':
                # fast speed
                self.game_speed = 750
        elif self.game_speed == 250:
            if up_down == 'down':
                # normal speed
                self.game_speed = 500
        elif self.game_speed == 750:
            if up_down == 'up':
                # normal speed
                self.game_speed = 500

    def show_settings(self):
        self.game.check_events()
        if self.game.ESCAPE_KEY:
            self.game.ESCAPE_KEY = False
            self.game.settings_prompt = False
        self.game.draw_interface()
        self.game.display.blit(IMAGES['settings_prompt'], (204, 256))
        self.buttons['speed_down'] = self.game.display.blit(IMAGES['speed_down'], (362, 352))
        self.buttons['speed_up'] = self.game.display.blit(IMAGES['speed_up'], (618, 352))
        self.buttons['music_down'] = self.game.display.blit(IMAGES['music_down'], (362, 462))
        self.buttons['music_up'] = self.game.display.blit(IMAGES['music_up'], (618, 462))
        self.buttons['music_mute'] = self.game.display.blit(IMAGES['music_mute'], (490, 572))
        self.game.draw_text(f'{self.game_speed_string()}', 30, 526, 390, text_format='c', text_color='white')
        self.game.draw_text(f'{self.music_volume:.1f}', 30, 526, 500, text_format='c', text_color='white')
        pygame.mixer.music.set_volume(self.music_volume)
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def game_speed_string(self):
        if self.game_speed == 750:
            return 'slow'
        elif self.game_speed == 500:
            return 'normal'
        elif self.game_speed == 250:
            return 'fast'

    def mute_music(self):
        self.music_volume = 0 if self.music_mute else self.music_volume

    def click_button(self, button):
        if button == self.buttons['speed_down']:
            self.change_speed('down')
        elif button == self.buttons['speed_up']:
            self.change_speed('up')
        elif button == self.buttons['music_down']:
            if self.music_volume >= 0.1:
                self.music_volume -= 0.1
                if self.music_volume == 0:
                    self.music_mute = True
        elif button == self.buttons['music_up']:
            if self.music_volume < 1.0:
                self.music_volume += 0.1
        elif button == self.buttons['music_mute']:
            if self.music_mute:
                self.music_mute = False
                self.music_volume = 1.0
            else:
                self.music_mute = True
                self.music_volume = 0

    def events_on_map(self):
        # tuple position of the player
        position = self.game.player.matrix_position(self.game.player.position[0], self.game.player.position[1])
        if position in self.map_events['extra_money']:
            self.map_events['extra_money'].remove(position)
            self.game.player.money += 25
        elif position in self.map_events['extra_exp']:
            self.map_events['extra_exp'].remove(position)
            self.game.player.experience += 50
        elif position in self.map_events['extra_sp']:
            self.map_events['extra_sp'].remove(position)
            skill = choice([s for s in self.game.player.skills])
            self.game.player.skills[skill] += 2
        elif position in self.map_events['extra_moves']:
            self.map_events['extra_moves'].remove(position)
            self.game.player.moves += 3
