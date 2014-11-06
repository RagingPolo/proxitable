from BtlBoard import BtlBoard
from BtlInputAbstract import BtlInputAbstract
# ------------------------------------
# CLASS BtlPlayer                    |
#                                    |
# Maintains state of a single player |
# and provides IO modules            |
# ------------------------------------

class BtlPlayer( object ):
  
  def __init__( self, name, bsize ):
    self.__name    = str( name )
    self.__board   = BtlBoard( int( bsize ) )
    self.__input   = None
    self.__history = list()
    self.__board.positionShips()

  # Should not be allowed once the game has started
  def repositionShips( self ):
    if len( self.__history ) == 0:
      self.__board.positionShips()

  def setInput( self, _input ):
    if isinstance( _input, BtlInputAbstract ):
      self.__input = _input
    else:
      raise TypeError( 'BtlPlayer.setInput() - invalid input module' )
    pass
  
  def getName( self ):
    return self.__name

  def getMoveHistory( self ):
    return self.__history

  def getLastMove( self ):
    if len( self.__history ) > 0:
      return self.__history[ -1 ]
    else:
      return None

  def getNextMove( self ):
    if self.__input is None:
      self.__history.append( self.__input.getMove() )
    else:
      raise Exception( 'BtlPlayer.getMove() - No input module set' )
# ------------------------------------
