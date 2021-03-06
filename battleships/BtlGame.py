from BtlPlayer import BtlPlayer
from BtlInputAbstract import BtlInputAbstract
from BtlOutputAbstract import BtlOutputAbstract
from time import sleep
# ------------------------------------
# CLASS BtlGame                      |
#                                    |
# Run game trun by turn and enforce  |
# game logic and check for winner    |
# ------------------------------------
class BtlGame( object ):

  def __init__( self, bsize ):
    self.P1 = 1
    self.P2 = 2
    self.__players = { self.P1 : BtlPlayer( 'Player 1', int( bsize ) ),
                       self.P2 : BtlPlayer( 'Player 2', int( bsize ) ) }
    self.__output = None

  def run( self ):
    # TODO something to display staring position
    # of ships and let the player re position until 
    # they are happy
    winner = 0
    while winner == 0:
      self.__showState( self.P1 )
      # Get P1 move
      self.__players[ self.P1 ].getNextMove( self.__players[ self.P2 ].getBoard() )
      if self.__players[ self.P1 ].getInput().isAi() is True:
        sleep( 1 )
      self.__showState( self.P1 )
      winner = self.__hasWinner()
      if winner == 0:
        # Get P2 move if ai pause
        self.__players[ self.P2 ].getNextMove( self.__players[ self.P1 ].getBoard() )
        if self.__players[ self.P2 ].getInput().isAi() is True:
          sleep( 1 )
        self.__showState( self.P1 )
        winner = self.__hasWinner()
    # there is a winner,do winner stuff
    self.__output.displayWinner( self.__players[ winner ] )


  def setInput( self, player, _input ):
    if isinstance( _input, BtlInputAbstract ):
      if player in [ self.P1, self.P2 ]:
        self.__players[ player ].setInput( _input )
      else:
        raise TypeError( 'BtlGame.setInput() - Unknown player' )
    else:
      raise TypeError( 'BtlGame.setInput() - Invalid input module' )

  def setOutput( self, output ):
    if isinstance( output, BtlOutputAbstract ):
      self.__output = output
    else:
      raise TypeError( 'BtlGame.setOutput() - Invalid output module' )

  # Internal method to display the current
  # game state from 'player' perspective
  def __showState( self, player ):
    if self.__output is not None:
      if player in [ self.P1, self.P2 ]:
        if player == self.P1:
          self.__output.showState( self.__players[ self.P1 ], self.__players[ self.P2 ] )
        else:
          self.__output.showState( self.__players[ self.P2 ], self.__players[ self.P1 ] )
      else:
        raise TypeError( 'BtlGame.showState() - Unknown player' )
    else:
      raise Exception( 'BtlGame.showState() - No output module set' )

  # Internal method to check if there 
  # is a winner after a turn
  # Returns 0 - No winner
  #         1 - player 1 has won
  #         2 - player 2 has won
  def __hasWinner( self ):
    if self.__players[ self.P1 ].getBoard().isAllSunk() is True:
      return self.P2
    elif self.__players[ self.P2 ].getBoard().isAllSunk() is True:
      return self.P1
    return 0
# ------------------------------------
