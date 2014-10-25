# -----------------------------------------------------------------
# Citidel game - written in python 3                              |
#                                                                 |
# Requires lib 'colorama' install with pip: pip3 install colorama |
#                                                                 |
# To run game: python3 path/to/Citadel.py                         |
#                                                                 |
# Simple ASCII output provided for testing, GPIO output method    |
# is currently a stub to be finished when electronics are known   |
# -----------------------------------------------------------------

# ------------------------------------
# CLASS CitPlayer                    |
#                                    |
# Maintains state of a single player |
# ------------------------------------
import os
import numbers
import getpass
from colorama import init, Fore

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

  OUTPUT = [ 'ASCII', 'GPIO' ]

  def __init__( self ):
    init() # Colorama init
    self._board = CitBoard()
    self._p1 = CitPlayer()
    self._p2 = CitPlayer()
    self._output = CitGame.OUTPUT.index( 'ASCII' )
  
  def run( self ):
    winner = self.hasWinner()
    while winner == 0:
      self.display()
      self.move( getMove( 'Player 1' ), getMove( 'Player 2' ) )
      winner = self.hasWinner()
    self.display()
    if winner == 1:
      print( '          Player 1 Wins!' )
    elif winner == 2:
      print( '          Player 2 Wins!' )
    else:
      print( '               Draw' )
    print()

  def setOutput( self, output ):
    try:
      x = CitGame.OUTPUT.index( output )
      self._output = x
    except ValueError as e:
      pass
    
  # Play out a turn of the game
  # p1m : Player ones move
  # p2m : Player twos move
  def move( self, p1m, p2m ):
    if ( isinstance( p1m, numbers.Number ) and
         isinstance( p2m, numbers.Number ) ):
      self._p1.addMove( p1m )
      self._p2.addMove( p2m )
      if p1m > p2m:
        self._board.moveRight()
      elif p2m > p1m:
        self._board.moveLeft()
    else:
      raise Exception( 'CitGame.move(): Not a number' );

  # Check if there == a winner
  # returns 0 : game not finished
  #         1 : player one
  #         2 : player two
  #         3 : draw
  def hasWinner( self ):
    if self._board.getPosition() == CitBoard.MAX:
      return 1
    if self._board.getPosition() == CitBoard.MIN:
      return 2
    if self._p1.hasLost():
      if self._p2.canWin( self._board.getPosition() ):
        while self._board.getPosition() > CitBoard.MIN:
          self._p2.addMove( 1 )
          self._board.moveLeft()
        return 2
      else:
        return 3
    if self._p2.hasLost():
      if self._p1.canWin( CitBoard.MAX - self._board.getPosition() ):
        while self._board.getPosition() < CitBoard.MAX:
          self._p1.addMove( 1 )
          self._board.moveRight()
        return 1
      else:
        return 3
    return 0

  def display( self ):
    if self._output == CitGame.OUTPUT.index( 'ASCII' ):
      self._asciiDisplay()
    elif self._output == CitGame.OUTPUT.index( 'GPIO' ):
      self._gpioDisplay()

  def _asciiDisplay( self ):
    os.system( 'cls' if os.name == 'nt' else 'clear' ) 
    print( Fore.CYAN + '   P1[' + Fore.RED + '{0:2d}'.format( self._p1.getPoints() ) + Fore.CYAN + ']' + Fore.WHITE +
           '-->         <--' + Fore.CYAN + '[' + Fore.RED + '{0:2d}'.format( self._p2.getPoints() ) + Fore.CYAN + ']P2' )
    print( Fore.YELLOW + '                |' )
    print( '            | - | - |' )
    print( '        |- -|- -|- -|- -|' )
    pos = self._board.getPosition()
    if pos == 0:
      print( ' --[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 1:
      print( ' --[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 2:
      print( ' --[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 3:
      print( ' --[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]--' )
    elif pos == 4:
      print( ' --[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]--' )
    elif pos == 5:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]--' )
    elif pos == 6:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']--' )
    print( '        |- -|- -|- -|- -|' )
    print( '            | - | - |' )
    print( '                |' + Fore.RESET )
    print()

  def _gpioDisplay( self ):
    pass

# ------------------------------------

# Get move from human
def getMove( name ):
  success = False
  while not success:
    move = getpass.getpass( Fore.WHITE + ' ' + name + ' enter move: ' + Fore.RESET )
    try:
      int_move = int( move )
      success = True
    except:
      pass
  return int_move

# Main -------------------------------
game = CitGame()
#game.setOuput( 'GPIO' )
game.run()
