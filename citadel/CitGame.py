import CitPlayer as CP
import CitBoard as CB
import CitOutAbstract
import numbers
import getpass
# ------------------------------------
# CLASS CitGame                      |
#                                    |
# Contains game logic and maintains  |
# overall game state                 |
# ------------------------------------
class CitGame( object ):

  def __init__( self ):
    self.__board = CB.CitBoard()
    self.__p1 = CP.CitPlayer()
    self.__p2 = CP.CitPlayer()
    self.__output = None
  
  def run( self ):
    winner = self.hasWinner()
    while winner == 0:
      self.showState()
      self.move( getMove( 'Player 1' ), getMove( 'Player 2' ) )
      winner = self.hasWinner()
    self.showState()
    self.showResult()

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
      self.__p1.addMove( p1m )
      self.__p2.addMove( p2m )
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
    if self.__p1.hasLost():
      if self.__p2.canWin( self.__board.getPosition() ):
        while self.__board.getPosition() > CB.CitBoard.MIN:
          self.__p2.addMove( 1 )
          self.__board.moveLeft()
        return 2
      else:
        return 3
    if self.__p2.hasLost():
      if self.__p1.canWin( CB.CitBoard.MAX - self.__board.getPosition() ):
        while self.__board.getPosition() < CB.CitBoard.MAX:
          self.__p1.addMove( 1 )
          self.__board.moveRight()
        return 1
      else:
        return 3
    return 0

  def showState( self ):
    if self.__output is not None:
      self.__output.showState( self.__board.getPosition(),
                               self.__p1.getPoints(), 
                               self.__p2.getPoints(),
                               self.__p1.getLastMove(),
                               self.__p2.getLastMove() )

  def showResult( self ):
    if self.__output is not None:
      self.__output.showResult( self.hasWinner() )
# ------------------------------------

# Get move from human
def getMove( name ):
  success = False
  while not success:
    move = getpass.getpass( ' ' + name + ' enter move: ' )
    try:
      int_move = int( move )
      success = True
    except:
      pass
  return int_move
