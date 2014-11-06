from abc import ABCMeta, abstractmethod
# ------------------------------------
# ABSTRACT CLASS BtlOutputAbstract   |
#                                    |
# Provide output for the game,       |
# display two boards based on        |
# current game state and result when |
# there is a winner                  |
# ------------------------------------
class BtlOutputAbstract( object ):
  
  @abstractmethod
  def displayBoards( self ):
    pass

  @abstractmethod
  def displayWinner( self ):
    pass
# ------------------------------------
