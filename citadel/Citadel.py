# -----------------------------------------------------------------
# Citidel game - written in python 3                              |
#                                                                 |
# To run game: python3 path/to/Citadel.py                         |
# -----------------------------------------------------------------
import CitGame
# Import desired output class here
import CitOutAscii as output

game = CitGame.CitGame()
game.setOutput( output.CitOutAscii() )
game.run()
