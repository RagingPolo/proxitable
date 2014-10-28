#!/usr/local/bin/python3
# -----------------------------------------------------------------
# Citidel game - written in python 3                              |
#                                                                 |
# To run game: python3 path/to/Citadel.py                         |
# -----------------------------------------------------------------
import CitGame
# Import desired output class here
import CitOutAscii as output
# Import desired imput classes here
import CitInTerminal as input1
import CitInBot as input2
# -----------------------------------------------------------------
game = CitGame.CitGame()
game.setInput( 1, input1.CitInTerminal() ) 
game.setInput( 2, input2.CitInBot( '.CitBot.pkl', 10 ) ) 
game.setOutput( output.CitOutAscii() )
game.run()
# -----------------------------------------------------------------
