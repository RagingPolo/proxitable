# ---------------------------------------------------------------------------- #
# CLASS CitBoard
#
# Maintains state of the citadel game board, board consists of 7 positions
# ---------------------------------------------------------------------------- #
class CitBoard( object ):
  
  MIN = 0 # Lowest board position
  MAX = 6 # Highest board position
  MID = 3 # Starting board postion

  # Start the board in the middle position
  def __init__( self ):
    self.__pos = CitBoard.MID

  # Get the current board position
  #  @returns - position
  def getPosition( self ):
    return self.__pos

  # If possible will move the board position one left
  def moveLeft( self ):
    if self.__pos > CitBoard.MIN:
      self.__pos -= 1

  # If possible will move the board position one right
  def moveRight( self ):
    if self.__pos < CitBoard.MAX:
      self.__pos += 1
# ---------------------------------------------------------------------------- #
