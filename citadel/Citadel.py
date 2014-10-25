# -----------------------------------------------------------------
# Citidel game - written in python 3                              |
#                                                                 |
# To run game: python3 path/to/Citadel.py                         |
# -----------------------------------------------------------------
import numbers
import getpass
import CitOutAbstract
# Import desired output class here
#import ???

# ------------------------------------
# CLASS CitPlayer                    |
#                                    |
# Maintains state of a single player |
# ------------------------------------
class CitPlayer( object ):
  
  def __init__( self ):
    self._points = 50
    self._moves  = list()

  def getPoints( self ):
    return self._points

  def addMove( self, move ):
    if isinstance( move, numbers.Number ):
      if self._points < move:
        self._points -= self._points
      else:
        self._points -= move
      self._moves.append( move )
    else:
      raise Exception( 'CitPlayer.addMove(): Not a number' );
 
  def getLastMove( self ):
    return self._moves[ -1 ]

  def hasLost( self ):
    if self._points > 0:
      return False
    else:
      return True

  def canWin( self, movesToWin ):
    if isinstance( movesToWin, numbers.Number ):
      if self._points < movesToWin:
        return False
      else:
        return True
    else:
      raise Exception( 'CitPlayer.canWin: Not a number' );
# ------------------------------------

# ------------------------------------
# CLASS CitBoard                     |
#                                    |
# Maintains state of game board      |
# ------------------------------------
class CitBoard( object ):
  
  MIN = 0
  MAX = 6
  MID = 3

  def __init__( self ):
    self._pos = CitBoard.MID

  def getPosition( self ):
    return self._pos

  def moveLeft( self ):
    if self._pos > CitBoard.MIN:
      self._pos -= 1

  def moveRight( self ):
    if self._pos < CitBoard.MAX:
      self._pos += 1
# ------------------------------------

# ------------------------------------
# CLASS CitGame                      |
#                                    |
# Contains game logic and maintains  |
# overall game state                 |
# ------------------------------------
class CitGame( object ):

  def __init__( self ):
    self.__board = CitBoard()
    self.__p1 = CitPlayer()
    self.__p2 = CitPlayer()
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
    if isinstance( output, CitOutAbstract ):
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
    if self.__board.getPosition() == CitBoard.MAX:
      return 1
    if self.__board.getPosition() == CitBoard.MIN:
      return 2
    if self.__p1.hasLost():
      if self.__p2.canWin( self.__board.getPosition() ):
        while self._board.getPosition() > CitBoard.MIN:
          self.__p2.addMove( 1 )
          self.__board.moveLeft()
        return 2
      else:
        return 3
    if self.__p2.hasLost():
      if self.__p1.canWin( CitBoard.MAX - self.__board.getPosition() ):
        while self.__board.getPosition() < CitBoard.MAX:
          self.__p1.addMove( 1 )
          self.__board.moveRight()
        return 1
      else:
        return 3
    return 0

  def showState( self ):
    if self.__output is not None:
      self.__output.showState()

  def showResult( self ):
    if self.__output is not None:
      self.__output.showResult()
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

# Main -------------------------------
game = CitGame()
game.run()
