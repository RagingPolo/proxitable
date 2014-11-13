from BtlInputAbstract import BtlInputAbstract
from BtlMove import BtlMove
import string
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
  
  def getMove( self ):
    valid = False
    while valid is False:
      xy = input( 'Enter move: ' )
      if ( xy[ : 1 ].upper() in string.ascii_uppercase[ : self.__size ] and
           xy[ 1 : ] in string.digits and
           int( xy[ 1 : ] ) in range( 1, self.__size + 1 ) ):
        valid = True
    return BtlMove( xy[ : 1 ], xy[ 1 : ] )
