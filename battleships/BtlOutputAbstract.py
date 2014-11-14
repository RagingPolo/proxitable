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
  
  # Display two boards from the perspective
  # of 'player'
  # @player - BtlPlayer object 
  # @opposition - BtlPlayer object
  @abstractmethod
  def showState( self, player, opposition ):
    pass

  # Display a message to convey the
  # winner of the game
  # @player - BtlPlayer object of winner
  @abstractmethod
  def displayWinner( self, player ):
    pass
# ------------------------------------
