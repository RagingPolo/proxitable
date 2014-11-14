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

  def getInput( self ):
    if self.__input is not None:
      return self.__input
    else:
      raise Exception( 'BtlPlayer().getInput() - No input set' )

  def getName( self ):
    return self.__name

  def getMoveHistory( self ):
    return self.__history

  def getBoard( self ):
    return self.__board

  def getLastMove( self ):
    if len( self.__history ) > 0:
      return self.__history[ -1 ]
    else:
      return None
  
  # Get the players next move using the
  # player input and take the shot
  # returns True  if a hit
  #         False if a miss
  def getNextMove( self, opBoard ):
    if self.__input is not None:
      lastMoveHit = self.getLastMove().wasHit() if len( self.__history ) > 0 else False
      self.__history.append( self.__input.getMove( lastMoveHit ) )
      hit = opBoard.takeShot( self.getLastMove() ) 
      self.getLastMove().setHit( hit )
      return hit
    else:
      raise Exception( 'BtlPlayer.getMove() - No input module set' )
# ------------------------------------
