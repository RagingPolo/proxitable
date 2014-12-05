#!/usr/local/bin/python3
# -----------------------------------------------------------------
# Citidel game - written in python 3                              |
#                                                                 |
# To run game: python3 path/to/Citadel.py                         |
# -----------------------------------------------------------------
import CitGame
# Import desired output class here
from CitOutSock import CitOutSock as Output
# Import desired imput classes here
from CitInTerminal import CitInTerminal as Input1
from CitInBot import CitInBot as Input2
# -----------------------------------------------------------------
game = CitGame.CitGame()
game.setInput( 1, Input1() ) # '.CitBot2.pkl', 3 ) ) 
game.setInput( 2, Input2( '.CitBot.pkl', 10 ) ) 
game.setOutput( Output( '127.0.0.1', 9000 ) )
game.run()
# -----------------------------------------------------------------
