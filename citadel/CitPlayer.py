import numbers
# ---------------------------------------------------------------------------- #
# CLASS CitPlayer
#
# Maintains state of a single player in the citadel game
# ---------------------------------------------------------------------------- #
class CitPlayer( object ):
  
  # Setup a new player with base starting values
  #  @name - name of the player
  def __init__( self, name ):
    self.__points = 50
    self.__moves  = list()
    self.__name = str( name )

  # Overrides object.__str__() to display the state of the player instance
  #  @returns - string
  def __str__( self ):
    return 'Citadel Player ' + self.getName() + ': ' + str( self.__points )
  
  # Add the next move to the players move history and adjust the remaining
  # points accordingly. It is up to the input method to ensure that the move
  # is a valid move
  def addMove( self, move ):
    if isinstance( move, numbers.Number ):
      if self.__points < move:
        self.__points -= self.__points
      else:
        self.__points -= move
      self.__moves.append( move )
    else:
      raise Exception( 'CitPlayer.addMove(): Not a number' );
 
  # Get the last move played by the player
  #  @returns - last move or None if there hasn't been one
  def getLastMove( self ):
    if len( self.__moves ) > 0:
      return self.__moves[ -1 ]
    else:
      return None

  # Check if the player has run out of points
  #  @returns - True if they have or False if they are still alive
  def hasLost( self ):
    if self.__points > 0:
      return False
    else:
      return True

  # Check if the player can mathematically still win from the current board position
  #  @returns - True if the can else False
  def canWin( self, movesToWin ):
    if isinstance( movesToWin, numbers.Number ):
      if self.__points < movesToWin:
        return False
      else:
        return True
    else:
      raise Exception( 'CitPlayer.canWin: Not a number' );
  
  # Get the players currents remaining points total
  #  @returns - remaining points
  def getPoints( self ):
    return self.__points

  # Get the name of the player
  #  @returns - players name
  def getName( self ):
    return self.__name
# ---------------------------------------------------------------------------- #
