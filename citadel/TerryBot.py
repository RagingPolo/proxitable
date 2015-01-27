from CitInAbstract import CitInAbstract
from os import urandom
import random
import pickle
import atexit
from enum import Enum
# ---------------------------------------------------------------------------- #
# CLASS TerryBot
#
# Class creates Terry Bot moves
# ---------------------------------------------------------------------------- #
class TerryBot( CitInAbstract ):

  # Set up a class instance including class attributes
  #  @args - empty list (this allows for the use of the generic module loader)
  def __init__( self, args ):
    # Set as a ai player input
    super().__init__( True )
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
    # Store class attributes
    self.__pos          = 3
    self.__opPoints     = 50
    self.__startPoints  = 50
    self.__onethird     = 1/3
    self.__twothird     = 2/3
    self.__onequarter   = 1/4
    self.__twoquarter   = 2/4
    self.__threequarter = 3/4
    # Setup mode
    self.__opLast = list()
    self.__mode = Enum( 'mode', 'UNK DEF AGR' )
    self.__opMode = self.__mode.UNK

  # Updates historic data, attempts to judge opponents play style and the works
  # out the next move to play
  #  @returns - players next move
  def getMove( self, name, points, last=None ):
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
    random.seed()
    move = 0
    if self.__pos == 1:
      if points < self.__opPoints:
        move = points
      elif ( points * self.__onequarter ) > self.__opPoints:
        move = points * self.__onequarter
      elif ( points * self.__onethird ) > self.__opPoints:
        move = points * self.__onethird
      elif ( points * self.__twoquarter ) > self.__opPoints:
        move = points * self.__twoquarter
      elif ( points * self.__twothird ) > self.__opPoints:
        move = points * self.__twothird
      elif ( points * self.__threequarter ) > self.__opPoints:
        move = points * self.__threequarter
      else:
        move = random.choice( [ points * self.__threequarter, points *
                                                             self.__twothird ] )
    elif self.__pos == 2:
      if ( points * self.__twothird ) < self.__opPoints:
        move = points * self.__onethird
      elif ( points * self.__threequarter ) < self.__opPoints:
        move = points * self.__onequarter
      elif points < self.__opPoints: 
        move = random.choice( [ points * self.__threequarter, points *
                                 self.__twothird, points * self.__twoquarter ] )
      elif points > self.__opPoints:
        move = random.choice( [ points * self.__twoquarter, points *
                                 self.__onethird, points * self.__onequarter ] )
      else:
        move = random.choice( [ points * self.__onequarter, points *
                                                             self.__onethird ] )
    elif self.__pos == 3:	
      if points == self.__startPoints:
        move = random.choice( [ random.randint( 1, 3 ), random.randint( 5, 7 ),
                                                      random.randint( 9, 12) ] )
      # TODO need history in to see where coming from to decide on how to play
      elif ( ( points * self.__twothird ) > ( self.__opPoints *
                                                        self.__threequarter ) ):
        move = ( points * self.__twothird ) - ( points * self.__onequarter )
      else:
        move = random.choice( [ points * self.__onequarter, points *
                                                             self.__onethird ] )
    elif self.__pos == 4:
      if ( points * self.__onethird ) > self.__opPoints:
        move = points * self.__twothird
      elif ( points * self.__onequarter ) > self.__opPoints:
        move = points * self.__threequarter
      elif points > self.__opPoints: 
        move = random.choice( [ points * self.__threequarter, points *
                                 self.__twothird, points * self.__twoquarter ] )
      elif points < self.__opPoints:
        move = random.choice( [ points * self.__twoquarter, points *
                                 self.__onethird, points * self.__onequarter ] )
      else:
        move = random.choice( [ points * self.__onequarter, points *
                                                             self.__onethird ] )
    elif self.__pos == 5:
      if points > self.__opPoints:
        move = self.__opPoints + 1		
      elif points < ( self.__opPoints * self.__onequarter ):
        move = points * self.__onequarter
      elif points < ( self.__opPoints * self.__onethird ):
        move = points * self.__onethird
      elif ( ( points * self.__threequarter ) < ( self.__opPoints *
                                                            self.__twothird ) ):
        move = points * self.__twothird
      else:
        move = random.choice( [ points * self.__onequarter, points *
                                                             self.__onethird ] )
    if int( move ) == 0:
      move += 1
    return int( move )	
# ---------------------------------------------------------------------------- #
