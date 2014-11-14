from abc import ABCMeta, abstractmethod
# ------------------------------------
# ABSTRACT CLASS BtlInputAbstract    |
#                                    |
# Provides a players move for each   |
# turn of the game                   |
# ------------------------------------
class BtlInputAbstract( object ):
  
  # Record if this is an ai player input
  # All sub classes should call super.__init__( ai )
  def __init__( self, ai ):
    self.__ai = ai

  # Get a players move for the turn
  # must RETURN a valid BtlMove
  # object
  @abstractmethod
  def getMove( self, lastMoveHit ):
    pass

  def isAi( self ):
    if self.__ai is True:
      return True
    return False
# ------------------------------------
