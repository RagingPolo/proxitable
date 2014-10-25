import numbers
# ------------------------------------
# CLASS CitPlayer                    |
#                                    |
# Maintains state of a single player |
# ------------------------------------
class CitPlayer( object ):
  
  def __init__( self ):
    self.__points = 50
    self.__moves  = list()

  def getPoints( self ):
    return self.__points

  def addMove( self, move ):
    if isinstance( move, numbers.Number ):
      if self.__points < move:
        self.__points -= self.__points
      else:
        self.__points -= move
      self.__moves.append( move )
    else:
      raise Exception( 'CitPlayer.addMove(): Not a number' );
 
  def getLastMove( self ):
    if len( self.__moves ) > 0:
      return self.__moves[ -1 ]
    else:
      return None

  def hasLost( self ):
    if self.__points > 0:
      return False
    else:
      return True

  def canWin( self, movesToWin ):
    if isinstance( movesToWin, numbers.Number ):
      if self.__points < movesToWin:
        return False
      else:
        return True
    else:
      raise Exception( 'CitPlayer.canWin: Not a number' );
# ------------------------------------
