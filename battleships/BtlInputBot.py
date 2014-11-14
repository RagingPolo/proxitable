from BtlInputAbstract import BtlInputAbstract
from BtlMove import BtlMove
from os import urandom
import random
# ------------------------------------
# CLASS BtlInpuBot                   |
#                                    |
# Bot Battleships player             |
# ------------------------------------
class BtlInputBot( BtlInputAbstract ):
  
  # Size is current board size
  def __init__( self, size ):
    super().__init__( True )
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
    self.__history = list()
    self.__size = int( size )

  def getMove( self, lastMoveHit ):
    move = self.__randomMove()
    while move in self.__history:
      move = self.__randomMove()
    self.__history.append( move )
    return move

  def __randomMove( self ):
    x = random.randint( 0, self.__size - 1 )
    y = random.randint( 0, self.__size - 1 )
    return BtlMove.genMove( x, y ) 
# ------------------------------------
