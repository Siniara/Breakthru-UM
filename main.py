import pygame

from ai.players import (
    HumanPlayer,
    ItDeepPlayer,
    MiniMaxPlayer,
    NegaMaxPlayer,
    RandomPlayer,
    RandomPlayerPlus,
)
from breakthru.game import Game
from breakthru.settings import HEIGHT, MARGIN, SQUARE_SIZE, WIDTH

FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakthru")


# converts mouse position to game board position row, col
def get_mouse_pos(pos):
    x, y = pos
    row = y // (SQUARE_SIZE + MARGIN)
    col = (x // (SQUARE_SIZE + MARGIN)) - 1
    # print('pos', pos)
    # print(row,col)
    return row, col


def main():
    running = True
    clock = pygame.time.Clock()

    game = Game(screen)

    # SELECT PLAYERS
    # players = (HumanPlayer('S'), HumanPlayer('G'))
    # players = (HumanPlayer("S"), NegaMaxPlayer("G", 1, game))
    # players = (NegaMaxPlayer('G', 1, game), NegaMaxPlayer('S', 1, game))
    players = (HumanPlayer('G'), ItDeepPlayer('S', game, 5))
    # players = (ItDeepPlayer('G', game, 5), NegaMaxPlayer('S', 1, game))
    # players = (HumanPlayer('S'), ItDeepPlayer('G', game, 7))
    # players = (NegaMaxPlayer('G', 2, game), NegaMaxPlayer('S', 2, game))
    ##################

    game.players = players

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print('Game history, {} actions'.format(game.actions))
                # for i in game.history:
                #     print(i)
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game.turn.change_turn()
                    print("Manual turn change")
                if event.key == pygame.K_z:
                    if len(game.history) >= 1:
                        game.undo_move()
                if event.key == pygame.K_p:
                    players = (NegaMaxPlayer("G", 1, game), NegaMaxPlayer("S", 1, game))
                    game.players = players
                if event.key == pygame.K_r:
                    print("Game history, {} actions".format(game.actions))
                    for i in game.history:
                        print(i)
                    print("Reset Board")
                    game.reset()
                if event.key == pygame.K_h:
                    game.save_log()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(game.turn.current_board.king_pos)
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos)
                if game.winner is None:
                    game.init_move(row, col)
                # if game.winner:
                #     game.save_log()

        game.update()

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
