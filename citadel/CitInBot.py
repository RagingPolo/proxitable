import CitInAbstract
from os import urandom
import random
# ------------------------------------
# CLASS CitInBot                     |
#                                    |
# Class creates computyer player     |
# moves                              |
# ------------------------------------
class CitInBot( CitInAbstract.CitInAbstract ):

  def __init__( self ):
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
    # Load move history
    self.history = None

  def __del__( self ):
    # Save move history
    pass

  def getMove( self, name, points, last=None ):
    if points == 1:
      move = 1
    else:
      move = random.randrange( 1, points )    
    return move
