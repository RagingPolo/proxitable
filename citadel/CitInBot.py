import CitInAbstract
from os import urandom
import random
import pickle
# ------------------------------------
# CLASS CitInBot                     |
#                                    |
# Class creates computyer player     |
# moves                              |
# ------------------------------------
class CitInBot( CitInAbstract.CitInAbstract ):

  def __init__( self ):
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
    # Load move history
    self.__pos      = 3
    self.__opPoints = 50
    self.__myLast   = None
    try:
      with open( '.CitBot.pkl', 'rb' ) as fd:
        self.__history = pickle.load( fd )
    except FileNotFoundError:
      self.__history = list()

  def __del__( self ):
    # Save move history
    with open( '.CitBot.pkl', 'wb' ) as fd:
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
    # Calculate next move
    move = self.__calculateMove( points )
    self.__myLast = move
    return move

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
        move = self.opPoints + 1
      else:
        # Choose a move based on the oppenents average + a bit of random spice
        if ( count > 0 and total > 0 ):
          avg = total / count
          move = avg + random.randrange( -10, 10 )
          if move < 1:
            move = 1
          elif move > points:
            move = points
        else:
          # If all else fails, just pick a random number
          move = random.randrange( 1, points )
    return int( move )
