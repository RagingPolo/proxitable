from abc import ABCMeta, abstractmethod
# --------------------------------------------------------------------------- #
# ABSTRACT CLASS CitIn
#
# Defines required method for a valid input class for the citadel game
# --------------------------------------------------------------------------- #
class CitInAbstract:
  __metaclass__ = ABCMeta

  # Record if this is an ai player input. All sub classes should call 
  # super.__init__( ai )
  def __init__( self, ai ):
    self.__ai = ai
  
  # Get a players move 
  #  @name    - name of player entering move
  #  @points  - players current points total
  #  @last    - opponents last move ( to aid AI players )
  #  @returns - move ( positive integer no greater than points )
  @abstractmethod
  def getMove( self, name, points, last=None ):
    pass

  # Is the input module a human or computer player
  #  @returns - True if a computer player else False
  def isAi( self ):
    if self.__ai is True:
      return True
    return False
# --------------------------------------------------------------------------- #
