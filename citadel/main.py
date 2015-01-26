from AbstractGame import AbstractGame
from CitPlayer import CitPlayer
from CitBoard import CitBoard
from CitInAbstract import CitInAbstract
from CitOutAbstract import CitOutAbstract
import numbers
import logging
import sys
from time import sleep
# ------------------------------------
# CLASS CitGame                      |
#                                    |
# Contains game logic and maintains  |
# overall game state                 |
# ------------------------------------
class Main( AbstractGame ):

  def __init__( self ):
    self.P1 = 1
    self.P2 = 2
    self.__board = CitBoard()
    self.__player = { self.P1 : CitPlayer( 'Player 1' ), self.P2 : CitPlayer( 'Player 2' ) }
    self.__output = None
    self.__input = { self.P1 : None, self.P2 : None }

  def connect( self, addr ):
    if self.__output is not None:
      return self.__output.connect( addr )
    return False

  def __str__( self ):
    return self.getName()

  def getName( self ):
    return 'Citadel'

  def run( self ):
    logging.info( '%s ] [ Started', self.getName() )
    winner = self.hasWinner()
    self.newGame()
    while winner == 0:
      self.showState()
      if ( self.__input[ self.P1 ].isAi() is True or
           self.__input[ self.P2 ].isAi() is True ):
        sleep( 1 )
      self.move( self.getMove( self.P1 ), self.getMove( self.P2 ) )
      winner = self.hasWinner()
    self.showState()
    logging.info( '%s ] [ Player %d Wins', self.getName(), winner )
    self.showResult()
  
  # Set the desired move input module for the specified player ( P1 | P2 )
  def setInput( self, player, input_ ):
    if isinstance( input_, CitInAbstract ):
      try:
        self.__input[ player ] = input_
      except KeyError:
        logging.warning( '%s ] [ Not a valid player', self.getName() )
    else:
      logging.warning( '%s ] [ Not a valid input object: %s', self.getName(), str( input_ ) )

  def setOutput( self, output ):
    if isinstance( output, CitOutAbstract ):
      self.__output = output
    else:
      logging.warning( '%s ] [ Not a valid output object: %s', self.getName(), str( output ) )

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
      logging.info( '%s ] [ Player 1 move: %d, Player 2 move: %d, Current board position: %d', self.getName(), p1m, p2m, self.__board.getPosition() )
    else:
      logging.warning( '%s ] [ Move was not a number', self.getName() )

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
    if self.__player[ 1 ].hasLost():
      if self.__player[ 2 ].canWin( self.__board.getPosition() ):
        while self.__board.getPosition() > CitBoard.MIN:
          self.__player[ 2 ].addMove( 1 )
          self.__board.moveLeft()
        return 2
      else:
        return 3
    if self.__player[ 2 ].hasLost():
      if self.__player[ 1 ].canWin( CitBoard.MAX - self.__board.getPosition() ):
        while self.__board.getPosition() < CitBoard.MAX:
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
      opponent = self.P1
    # Try and call the players input module
    try:
      if self.__input[ player ] is not None:
        move = self.__input[ player ].getMove( self.__player[ player ].getName(),
                                               self.__player[ player ].getPoints(),
                                               self.__player[ opponent ].getLastMove() )
      else:
        logging.critical( '%s ] [ No input module for %s', self.getName(), self.__player[ player ].getName() )
        sys.exit( 1 )
    except KeyError:
      logging.warning( '%s ] [ Not a valid player', self.getName() )
    return move

  def newGame( self ):
    if self.__output is not None:
      self.__output.newGame()

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
