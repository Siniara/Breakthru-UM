from breakthru.game import Game
import time
from ai.players import RandomPlayer, RandomPlayerPlus, MiniMaxPlayer, NegaMaxPlayer, ItDeepPlayer

game = Game(None)
players = (NegaMaxPlayer('G',1,game), RandomPlayerPlus('S'))
# players = (ItDeepPlayer('S', game, 8), ItDeepPlayer('G', game, 8))
# players = (ItDeepPlayer('S', game, 8), MiniMaxPlayer('G', 1, game))
# players = (ItDeepPlayer('G', game, 8), MiniMaxPlayer('S', 1, game))
# players = (NegaMaxPlayer('S', 2, game), NegaMaxPlayer('G', 2, game))
game.players = players
start = time.time()
while game.winner is None:
    game.init_move()
    print('action:', game.actions)
end = time.time()
print('game time:', end - start)
