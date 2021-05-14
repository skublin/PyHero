from game import Game

g = Game()

while g.running:
    """
    This is the main loop to run the game.
    """
    g.curr_menu.display_menu()
    g.game_loop()
