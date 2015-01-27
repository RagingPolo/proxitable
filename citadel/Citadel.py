import CitOutTerminal as CitGame
# Import desired output class here
from CitOutTerminal import CitOutTerminal as Output
# Import desired imput classes here
from CitInTerminal import CitInTerminal as Input1
from CitInBotNew import CitInBotNew as Input2
# ---------------------------------------------------------------------------- #
# Standalone Citidel game tester
#
# To run game: python3 path/to/Citadel.py
# ---------------------------------------------------------------------------- #
game = CitGame.CitGame()
game.setInput( 1, Input1( [] ) ) ) ) 
game.setInput( 2, Input2( '.CitBot.pkl', 10 ) ) 
game.setOutput( Output() )
game.run()
# ---------------------------------------------------------------------------- #
