import pygame
from random import choice


# IT NEEDS TO BE REMOVED
# IMAGES ARE LOADED IN warrior.py FILE (!)
IMAGES = {f'{f}-{n}-{d}': pygame.image.load(f'graphics/warriors/{f}/{n}/{d}.png')
          for f in ['demon', 'elf', 'human', 'undead']
          for n in range(1, 8)
          for d in ['left', 'right']}

BUTTONS = {'next_unit': pygame.image.load('graphics/btn/next_unit.png'),
           'pointer': pygame.image.load('graphics/btn/pointer.png'),
           'battle_end': pygame.image.load('graphics/prompt_window.png')}


class Battle:
    def __init__(self, game, battle_map, interface_image, number, player, enemy):
        self.game = game
        self.battle_map = battle_map
        self.interface_image = interface_image
        self.number = number
        self.player = player
        self.enemy = enemy
        self.round = 1
        self.player_pointer, self.enemy_pointer = 1, 0
        self.amount = pygame.image.load('graphics/btn/amount_button.png')
        self.buttons = dict()
        self.player_clickable_warriors = dict()
        self.enemy_clickable_warriors = dict()

    def check_armies(self):
        return len(self.game.player.army) > 0, len(self.game.enemy.army) > 0

    def battle_loop(self):
        pygame.mixer.music.load("music/battle_music.ogg")
        pygame.mixer.music.play(-1)
        self.player_pointer, self.enemy_pointer = 1, 0
        while self.game.battle_mode:
            self.draw_battle_interface()
            self.game.check_events()
            # QUIT BATTLE PROMPT
            if self.game.ESCAPE_KEY:
                self.game.ESCAPE_KEY = False
                self.game.prompt = True
                self.open_prompt('Are you sure?', "You'll abandon the battle!")
                if self.game.prompt_answer:
                    if self.game.answer == 'yes':
                        self.game.prompt = False
                        self.quit_battle()
            # ENEMY ATTACK
            if 0 < self.enemy_pointer < 7:
                self.enemy_attack()
                self.enemy_pointer += 1
            elif self.enemy_pointer == 7:
                self.enemy_attack()
                self.enemy_pointer = 8
                self.player_pointer = 1
                if not self.player.warriors_alive(self.player_pointer):
                    self.next_unit_click()
                self.round += 1
                self.reset_done_attacks()
            # CHECK WINNERS
            if len(self.enemy.alive_in_army(self.enemy)) == 0:
                self.win_prompt()
            elif len(self.player.alive_in_army(self.player)) == 0:
                self.defeat_prompt()
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()
            self.game.reset_keys()

    def open_prompt(self, text, additional_text=''):
        yes = pygame.image.load('graphics/btn/yes_button.png')
        no = pygame.image.load('graphics/btn/no_button.png')
        window_image = pygame.image.load('graphics/prompt_window.png')
        while self.game.prompt:
            self.game.check_events()
            if self.game.ESCAPE_KEY:
                self.game.prompt = False
                self.game.prompt_answer = False
            elif self.game.START_KEY:
                self.game.prompt = False
                self.game.prompt_answer = True
            self.draw_battle_interface()
            self.game.display.blit(window_image, (204, 256))
            self.game.buttons['yes'] = self.game.display.blit(yes, (616, 350))
            self.game.buttons['no'] = self.game.display.blit(no, (358, 350))
            self.game.draw_text(text, 32, 524, 278, text_format='c')
            if len(additional_text) > 0:
                self.game.draw_text(additional_text, 32, 524, 314, text_format='c')
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()

    def draw_battle_interface(self):
        # it needs to be changed to proper battle interface (!)
        self.game.display.blit(self.battle_map, (12, 126))
        self.game.display.blit(self.interface_image, (0, 0))
        self.game.draw_text(f'{self.player.name}', 40, 26, 14, text_format='tl')
        self.game.draw_text(f'Round: {self.round}', 36, 768, 16, text_format='tl')
        self.buttons['next_unit'] = self.game.display.blit(BUTTONS['next_unit'], (942, 20))
        self.draw_armies()

    def draw_armies(self):
        for player_warrior, i in zip(self.player.army, range(1, 8)):
            if i % 2 == 0:
                # PLAYER'S WARRIORS
                if self.player.army[player_warrior] > 0:
                    self.player_clickable_warriors[f'{player_warrior.name}'] = self.game.display.blit(
                        IMAGES[f'{player_warrior.name}-right'], (128, 710 - (i - 1)*80))
                    self.game.display.blit(self.amount, (90, 738 - (i - 1) * 80))
                    self.game.draw_text(f'{self.player.army[player_warrior]}',
                                        22, 110, 756 - (i - 1) * 80, text_format='c', text_color='white')
                    if i == self.player_pointer:
                        self.game.display.blit(BUTTONS['pointer'], (100, 725 - (i - 1) * 80))
            else:
                # PLAYER'S WARRIORS
                if self.player.army[player_warrior] > 0:
                    self.player_clickable_warriors[f'{player_warrior.name}'] = self.game.display.blit(
                        IMAGES[f'{player_warrior.name}-right'], (80, 710 - (i - 1)*80))
                    self.game.display.blit(self.amount, (42, 738 - (i - 1) * 80))
                    self.game.draw_text(f'{self.player.army[player_warrior]}',
                                        22, 62, 756 - (i - 1) * 80, text_format='c', text_color='white')
                    if i == self.player_pointer:
                        self.game.display.blit(BUTTONS['pointer'], (52, 725 - (i - 1) * 80))
        for enemy_warrior, j in zip(self.enemy.army, range(1, 8)):
            if j % 2 == 0:
                # ENEMY'S WARRIORS
                if self.enemy.army[enemy_warrior] > 0:
                    self.enemy_clickable_warriors[f'{enemy_warrior.name}'] = self.game.display.blit(
                        IMAGES[f'{enemy_warrior.name}-left'], (892, 710 - (j - 1)*80))
                    self.game.display.blit(self.amount, (854, 738 - (j - 1) * 80))
                    self.game.draw_text(f'{self.enemy.army[enemy_warrior]}',
                                        22, 874, 756 - (j - 1) * 80, text_format='c', text_color='white')
                    if j == self.enemy_pointer:
                        self.game.display.blit(BUTTONS['pointer'], (864, 725 - (j - 1) * 80))
            else:
                # ENEMY'S WARRIORS
                if self.enemy.army[enemy_warrior] > 0:
                    self.enemy_clickable_warriors[f'{enemy_warrior.name}'] = self.game.display.blit(
                        IMAGES[f'{enemy_warrior.name}-left'], (940, 710 - (j - 1)*80))
                    self.game.display.blit(self.amount, (902, 738 - (j - 1) * 80))
                    self.game.draw_text(f'{self.enemy.army[enemy_warrior]}',
                                        22, 922, 756 - (j - 1) * 80, text_format='c', text_color='white')
                    if j == self.enemy_pointer:
                        self.game.display.blit(BUTTONS['pointer'], (912, 725 - (j - 1) * 80))

    def next_unit_click(self):
        if self.player_pointer < 7:
            self.player_pointer += 1
            if not self.player.warriors_alive(self.player_pointer):
                self.next_unit_click()
        elif self.player_pointer == 7:
            self.player_pointer = 8     # it's not 0, but 8 to avoid < 7 situation
            self.enemy_pointer = 1
            if not self.enemy.warriors_alive(self.enemy_pointer):
                self.next_unit_click()
        elif self.enemy_pointer < 7:
            self.enemy_pointer += 1
            if not self.enemy.warriors_alive(self.enemy_pointer):
                self.next_unit_click()
        elif self.enemy_pointer == 7:
            self.enemy_pointer = 8      # it's not 0, but 8 to avoid < 7 situation
            self.player_pointer = 1
            self.round += 1
            self.reset_done_attacks()
            if not self.player.warriors_alive(self.player_pointer):
                self.next_unit_click()

    def click_and_attack(self, defender, click_position):
        x, y = click_position
        if 0 < self.player_pointer < 8:
            for attacker, i in zip(self.player.army, range(1, 8)):
                if i == self.player_pointer and attacker.done_attack is False:
                    damage = attacker.damage_taken(defender)
                    if damage > defender.actual_health:
                        self.warrior_reduction(damage, defender, self.enemy)
                    elif damage == defender.actual_health:
                        self.enemy.army[defender] -= 1
                        if self.enemy.army[defender] > 0:
                            defender.actual_health = defender.health
                    else:
                        defender.actual_health -= damage
                    self.draw_battle_interface()
                    self.game.draw_text(f'-{damage}', 36, x + 20, y - 20, text_format='c', text_color='red')
                    print(f'{defender.name=}, {defender.health=}, {defender.actual_health=}')
                    self.game.window.blit(self.game.display, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.game.world.game_speed * 2)
                    attacker.done_attack = True

    def enemy_attack(self):
        if 0 < self.enemy_pointer < 8:
            defender = self.enemy.draw_warrior_to_attack(self.player)
            x = self.player_clickable_warriors[defender.name].left
            y = self.player_clickable_warriors[defender.name].top
            for attacker, i in zip(self.enemy.army, range(1, 8)):
                if i == self.enemy_pointer and self.enemy.warriors_alive(i):
                    damage = attacker.damage_taken(defender)
                    if damage > defender.actual_health:
                        self.warrior_reduction(damage, defender, self.player)
                    elif damage == defender.actual_health:
                        self.player.army[defender] -= 1
                        if self.player.army[defender] > 0:
                            defender.actual_health = defender.health
                    else:
                        defender.actual_health -= damage
                    self.draw_battle_interface()
                    self.game.draw_text(f'-{damage}', 36, x + 34, y + 48, text_format='c', text_color='red')
                    print(f'{defender.name=}, {defender.health=}, {defender.actual_health=}')
                    self.game.window.blit(self.game.display, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.game.world.game_speed * 4)

    @staticmethod
    def warrior_reduction(damage, target, character):
        available_health = target.health * (character.army[target] - 1) + target.actual_health
        left_health = available_health - damage
        if left_health > 0:
            full_warriors = left_health // target.health
            target.actual_health = left_health - full_warriors * target.health
            if target.actual_health == 0:
                target.actual_health = target.health
            character.army[target] = full_warriors + 1
        else:
            target.actual_health = target.health
            character.army[target] = 0

    def reset_done_attacks(self):
        for player_warrior, enemy_warrior in zip(self.player.army, self.enemy.army):
            player_warrior.done_attack = False
            enemy_warrior.done_attack = False

    def win_prompt(self):
        self.game.draw_interface()
        self.game.prompt = True
        self.game.open_prompt('Congratulations!', "You won the battle!")
        if self.game.prompt_answer:
            self.game.make_characters('enemy')
            self.enemy.position = choice(self.game.POSITIONS[0])
            self.game.turn += 1
            self.give_reward()
            self.quit_battle()
            self.game.prompt = False
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def defeat_prompt(self):
        self.game.draw_interface()
        self.game.prompt = True
        self.game.open_prompt("You're defeated!", "Wanna start again?")
        if self.game.prompt_answer:
            if self.game.answer == 'no':
                self.quit_battle()
                self.game.playing = False
                self.game.prompt = False
                self.game.curr_menu = self.game.MENUS['creator_menu']
                self.game.curr_menu.run_display = True
                pygame.mouse.set_visible(False)
                pygame.mixer.music.unload()
                pygame.mixer.music.load("music/menu_music.ogg")
                pygame.mixer.music.play(-1)
                self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
                self.game.window = pygame.display.set_mode((self.game.DISPLAY_W, self.game.DISPLAY_H))
            elif self.game.answer == 'yes':
                self.quit_battle()
                self.game.turn = 1
                self.game.make_characters('player')
                self.player.position = choice(self.game.POSITIONS[12])
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def quit_battle(self):
        self.game.battle_mode = False
        pygame.mixer.music.unload()
        pygame.mixer.music.load("music/game_music.ogg")
        pygame.mixer.music.play(-1)
        self.round = 1
        self.game.reset_keys()

    def give_reward(self):
        self.player.money += self.enemy.money
        self.player.experience += 80
        self.player.moves += 4
