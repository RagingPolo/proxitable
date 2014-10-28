from abc import ABCMeta, abstractmethod
# ------------------------------------
# ABSTRACT CLASS CitIn               |
#                                    |
# Defines required method for a      |
# valid input class.                 |
# ------------------------------------
class CitInAbstract:
  __metaclass__ = ABCMeta

  # Record if this is an ai player input
  # All sub classes should call super.__init__( ai )
  def __init__( self, ai ):
    self.__ai = ai
  
  # Get a players input, the method must
  # RETURN a positive integer value no
  # greater than points
  # name   : name of player entering move
  # points ; players current points total
  # last   : opponents last move ( to aid AI players )
  @abstractmethod
  def getMove( self, name, points, last=None ):
    pass

  def isAi( self ):
    if self.__ai is True:
      return True
    return False
# ------------------------------------
