from BtlInputAbstract import BtlInputAbstract
from BtlMove import BtlMove
import string
import numbers
# ------------------------------------
# CLASS BtlInpuBot                   |
#                                    |
# Bot Battleships player             |
# ------------------------------------
class BtlInputTerminal( BtlInputAbstract ):
  
  # Size is current board size
  def __init__( self, size ):
    super().__init__( False )
    self.__history = list()
    self.__size = int( size )
  
  def getMove( self, lastMoveHit ):
    valid = False
    while valid is False:
      xy = input( 'Enter move: ' )
      if xy[ : 1 ].upper() in string.ascii_uppercase[ : self.__size ]:
        if isinstance( int( xy[ 1 : ] ), numbers.Number ):
          if int( xy[ 1 : ] ) in range( 1, self.__size + 1 ):
            move = BtlMove( xy[ : 1 ], xy[ 1 : ] )
            if move not in self.__history:
              self.__history.append( move )
              valid = True
            else:
              print( 'You have already made that move' )
          else:
            print( 'y must be between 1 and ' + str( size ) )
        else:
          print( 'y must be a number' )
      else:
        print( 'x must be a letter' )
    return move
