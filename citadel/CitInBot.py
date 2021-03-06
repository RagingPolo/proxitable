from CitInAbstract import CitInAbstract
import random
import pickle
import atexit
from enum import Enum
from os import urandom
# ---------------------------------------------------------------------------- #
# CLASS CitInBot
#
# Class creates a computer player moves
# ---------------------------------------------------------------------------- #
class CitInBot( CitInAbstract ):

  # Set up the input class with all of the required starting values then
  # attempt to load a history file or create a new one
  #  @args - empty list (this allows for the use of the generic module loader)
  def __init__( self, args ):
    # Set as a ai player input
    super().__init__( True )
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
    # Store class attributes
    self.__pos      = 3
    self.__opPoints = 50
    self.__filename = args[ 0 ]
    self.__variance = int( args[ 1 ] )
    # Setup mode
    self.__opLast = list()
    self.__mode = Enum( 'mode', 'UNK DEF AGR' )
    self.__opMode = self.__mode.UNK
    # Load move history
    try:
      with open( self.__filename, 'rb' ) as fd:
        self.__history = pickle.load( fd )
    except FileNotFoundError:
      self.__history = list()
    atexit.register( self.saveHistory )

  # Save the internal records to file
  def saveHistory( self ):
    # Trim history list to at most last 100 turns
    if len( self.__history ) > 100:
      cut = len( self.__history ) - 101
      self.__history = self.__history[ cut : ]
    # Save move history
    with open( self.__filename, 'wb' ) as fd:
      pickle.dump( self.__history, fd )

  # Updates historic data, attempts to judge opponents play style and the works
  # out the next move to play
  #  @returns - players next move
  def getMove( self, name, points, last=None ):
    # Store last turn, if there was one, in history
    if last is not None:
      self.__history.append( [ points + self.__myLast, # 0
                               self.__opPoints,        # 1
                               self.__myLast,          # 2
                               last,                   # 3
                               self.__pos ] )          # 4
    # Update internal records
    if ( last is not None and self.__myLast is not None ):
      if self.__myLast > last:
        self.__pos += 1
      elif last > self.__myLast:
        self.__pos -= 1
      self.__opPoints -= last
    # Update opponents mode
    if len( self.__opLast ) == 3:
      self.__opLast = self.__opLast[ 1 : ]
    if last is not None:
      self.__opLast.append( last )
    if len( self.__opLast ) == 3:
      # At least 2 of the last 3 moves were very low
      if sum( x < 4 for x in self.__opLast ) > 1:
        self.__opMode = self.__mode.DEF
      # At least 2 of the last 3 moves were quite high  
      elif sum( x > 8 for x in self.__opLast ) > 1:
        self.__opMode = self.__mode.AGR
      # Neither
      else:
        self.__opMode = self.__mode.UNK
    # Calculate next move
    move = self.__calculateMove( points )
    self.__myLast = move
    return move

  # Calculate the next move based on current position, history and opponents 
  # play style
  #  @returns - players next move
  def __calculateMove( self, points ):
    # Check history for previous turns on this position
    total = 0
    count = 0
    for turn in self.__history:
      if turn[ 4 ] == self.__pos:
        total += turn[ 3 ]
        count += 1
    # If you only have a single point left, not much you can do
    if points == 1:
      move = 1
    else:
      # If you can definatly win, just win
      if ( self.__pos == 5 and points > self.__opPoints ):
        move = self.__opPoints + 1
      else:
        # Choose a move based on the oppenents average + a bit of random spice
        if ( count > 0 and total > 0 ):
          avg = total / count
          move = avg + random.randrange( 0 - self.__variance, self.__variance )
          if move < 1:
            move = 1
          elif move > points:
            move = points
          # Ajust move based on position and percieved opponent mode
          if self.__pos < 3:
            # Were losing!
            if self.__opMode == self.__mode.DEF:
              pass
            elif self.__opMode == self.__mode.AGR:
              move += 2
          else:
            # We're winning I guess
            if self.__opMode == self.__mode.DEF:
              move += 2
            elif self.__opMode == self.__mode.AGR:
              move -= 2
        else:
          # If all else fails, just pick a random number
          move = random.randrange( 1, points )
      if move > points:
        move = points
    return int( move )
# ---------------------------------------------------------------------------- #
