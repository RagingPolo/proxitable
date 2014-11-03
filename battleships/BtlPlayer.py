import BtlBoard
# ------------------------------------
# CLASS BtlPlayer                    |
#                                    |
# Maintains state of a single player |
# and provides IO modules            |
# ------------------------------------

class BtlPlayer( object ):
  
  def __init__( self, name ):
    self.__name   = str( name )
    self.__board  = BtlBoard.BtlBoard( 10 )
    self.__input  = None
    self.__output = None
    self.__board.positionShips()

  def setInput( self, _input ):
    pass

  def setOutput( self, output ):
    pass

  def getShot( self ):
    if self.__input is None:
      pass
    else:
      raise Exception( 'BtlPlayer.getShot() - No input module set' )
# ------------------------------------
