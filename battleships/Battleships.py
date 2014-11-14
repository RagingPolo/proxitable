from BtlGame import BtlGame
from BtlOutputTerminal import BtlOutputTerminal
from BtlInputTerminal import BtlInputTerminal
from BtlInputBot import BtlInputBot
from BtlInputStupidBot import BtlInputStupidBot

bsize = 10
game = BtlGame( bsize )
game.setOutput( BtlOutputTerminal() )
game.setInput( 1, BtlInputBot( bsize ) )
game.setInput( 2, BtlInputStupidBot( bsize ) ) 
game.run()
