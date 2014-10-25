from abc import ABCMeta, abstractmethod

# ------------------------------------
# ABSTRACT CLASS CitOut              |
#                                    |
# Defines required method for a      |
# valid output class                 |
# ------------------------------------
class CitOutAbstract:
  __metaclass__ = ABCMeta

  def __init__( self ):
    self.P1   = 1
    self.P2   = 2
    self.DRAW = 3

  # Display the current game state
  # pos : board position : 0-6 
  # p1p : player one points : 0-50
  # p2p : player two points : 0-50
  # p1m : player one last move : int
  # p2m : player two last move : int
  @abstractmethod
  def showState( self, pos, p1p, p2p, p1m, p2m ):
    pass
  
  # Display the game result
  # result : the game result : P1, P2, DRAW
  @abstractmethod
  def showResult( self, result ):
    pass
# ------------------------------------

