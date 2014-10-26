import CitPlayer as CP
import CitBoard as CB
import CitOutAbstract
import CitInAbstract
import numbers
# ------------------------------------
# CLASS CitGame                      |
#                                    |
# Contains game logic and maintains  |
# overall game state                 |
# ------------------------------------
class CitGame( object ):

  def __init__( self ):
    self.P1 = 1
    self.P2 = 2
    self.__board = CB.CitBoard()
    self.__player = { self.P1 : CP.CitPlayer(), self.P2 : CP.CitPlayer() }
    self.__output = None
    self.__input = { self.P1 : None, self.P2 : None }

  def run( self ):
    winner = self.hasWinner()
    while winner == 0:
      self.showState()
      self.move( self.getMove( self.P1 ), self.getMove( self.P2 ) )
      winner = self.hasWinner()
    self.showState()
    self.showResult()
  
  # Set the desired move input module for the specified player ( P1 | P2 )
  def setInput( self, player, input_ ):
    if isinstance( input_, CitInAbstract.CitInAbstract ):
      try:
        self.__input[ player ] = input_
      except KeyError:
        raise Exception( 'CitGame.setInput(): Not a valid player, use P1 - 1 or P2 - 2' )
    else:
      raise Exception( 'CitGame.setInput(): Not a valid input object' )
      

  def setOutput( self, output ):
    if isinstance( output, CitOutAbstract.CitOutAbstract ):
      self.__output = output
    else:
      raise Exception( 'CitGame.setOutput(): Not a valid output object' )

  # Play out a turn of the game
  # p1m : Player ones move
  # p2m : Player twos move
  def move( self, p1m, p2m ):
    if ( isinstance( p1m, numbers.Number ) and
         isinstance( p2m, numbers.Number ) ):
      # AddMove() must not be called until both players moves have been recieved
      self.__player[ 1 ].addMove( p1m )
      self.__player[ 2 ].addMove( p2m )
      if p1m > p2m:
        self.__board.moveRight()
      elif p2m > p1m:
        self.__board.moveLeft()
    else:
      raise Exception( 'CitGame.move(): Not a number' );

  # Check if there == a winner
  # returns 0 : game not finished
  #         1 : player one
  #         2 : player two
  #         3 : draw
  def hasWinner( self ):
    if self.__board.getPosition() == CB.CitBoard.MAX:
      return 1
    if self.__board.getPosition() == CB.CitBoard.MIN:
      return 2
    if self.__player[ 1 ].hasLost():
      if self.__player[ 2 ].canWin( self.__board.getPosition() ):
        while self.__board.getPosition() > CB.CitBoard.MIN:
          self.__player[ 2 ].addMove( 1 )
          self.__board.moveLeft()
        return 2
      else:
        return 3
    if self.__player[ 2 ].hasLost():
      if self.__player[ 1 ].canWin( CB.CitBoard.MAX - self.__board.getPosition() ):
        while self.__board.getPosition() < CB.CitBoard.MAX:
          self.__player[ 1 ].addMove( 1 )
          self.__board.moveRight()
        return 1
      else:
        return 3
    return 0

  # Get a move for the specified player using the players input module
  def getMove( self, player ):
    # Calculate opponent from player value, 
    opponent = 3 # if player is invalid opponent will stay invalid as 3
    if player == self.P1:
      opponent = self.P2
    elif player == self.P2:
      opponent == self.P1
    # Try and call the players input module
    try:
      if self.__input[ player ] is not None:
        # TODO add name attribute and associated methods to CitPlayer class
        self.__input[ player ].getMove( str( player ),
                                        self.__player[ player ].getPoints(),
                                        self.__player[ opponent ].getLastMove() )
      else:
        # TODO is there a way to make this an uncatchable fatal error?
        raise Exception( 'CitGame.getMove(): Fatal error - No input module provided for ' + str( player ) )
    except KeyError:
      raise Exception( 'CitGame.getMove(): Not a valid player, use P1 - 1 or P2 - 2' )

  def showState( self ):
    if self.__output is not None:
      self.__output.showState( self.__board.getPosition(),
                               self.__player[ 1 ].getPoints(), 
                               self.__player[ 2 ].getPoints(),
                               self.__player[ 1 ].getLastMove(),
                               self.__player[ 2 ].getLastMove() )

  def showResult( self ):
    if self.__output is not None:
      self.__output.showResult( self.hasWinner() )
# ------------------------------------
