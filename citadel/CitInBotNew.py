import CitInAbstract
from os import urandom
import random
import pickle
import atexit
from enum import Enum
# ------------------------------------
# CLASS CitInBot                     |
#                                    |
# Class creates computyer player     |
# moves                              |
# ------------------------------------
class CitInBot( CitInAbstract.CitInAbstract ):

  def __init__( self, args ):
    # Set as a ai player input
    super().__init__( True )
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
    # Store class attributes
    self.__pos = 3
    self.__opPoints = 50
    self.__filename = args[ 0 ]
    self.__variance = int( args[ 1 ] )
    self.__onethird = 1/3
    self.__twothirds = 2/3
    self.__onequarter = 1/4
    self.__twoquarter = 2/4
    self.__threequarter = 3/4
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

  def saveHistory( self ):
    # Trim history list to at most last 100 turns
    if len( self.__history ) > 100:
      cut = len( self.__history ) - 101
      self.__history = self.__history[ cut : ]
    # Save move history
    with open( self.__filename, 'wb' ) as fd:
      pickle.dump( self.__history, fd )

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

  def __calculateMove( self, points ):
    random.seed()
	
	# Check history for previous turns on this position
    total = 0
    count = 0
    for turn in self.__history:
      if turn[ 4 ] == self.__pos:
        total += turn[ 3 ]
        count += 1		
        if ( self.__pos == 1 ):
                # if loss is inevitable, lose
                if ( points < self.opPoints ):
                        move = points
                # if opponents points are less than one quarter, play one quarter of points
                elif ( ( points * self.__onequarter ) > self.opPoints ):
                        move = points * self.__onequarter
                # if opponents points are less than one third, play one third of points
                elif ( ( points * self.__onethird ) > self.opPoints ):
                        move = points * self.__onethird
                # if opponents points are less half, play one half of points
                elif ( ( points * self.__twoquarter ) > self.opPoints ):
                        move = points * self.__twoquarter
                # if opponents points are less than two thirds, play one third of points
                elif ( ( points * self.__twothirds ) > self.opPoints ):
                        move = points * self.__twothirds
                # if opponents points are less than three quarters, play three quarters of points
                elif ( ( points * self.__threequarter ) > self.opPoints ):
                        move = points * self.__threequarter
                ############################# placeholder move #############################
                else:
                        move = points * self.__twoquarter
        elif ( self.__pos == 2 ):
                # if opponents points are more than two thirds, play one third of points
                if ( ( points * self.__twothirds ) < self.opPoints ):
                        move = points * self.__onethird
                ############################# placeholder move #############################
                else:
                        move = points * self.__twoquarter
        elif ( self.__pos == 3 ):
                # if points are 50 at pos 3, must be start of game, random between 1 and 9	
                if ( points == 50 ):
                        random.randint(1,9)
                ############################# placeholder move #############################
                else:
                        move = points * self.__twoquarter
        elif ( self.__pos == 4 ):
                ############################# placeholder move #############################
                move = points * self.__twoquarter
        elif ( self.__pos == 5 ):
                # if win is possible, just win
                if ( points > self.__opPoints ):
                        move = self.__opPoints + 1		
                # otherwise, trick the opponent
                elif ( points < self.__opPoints ):
                        move = points * self.__onequarter
                ############################# placeholder move #############################
                else:
                        move = points * self.__twoquarter
        return int( move )	