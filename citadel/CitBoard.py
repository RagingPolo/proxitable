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
    self.__pos = CitBoard.MID

  def getPosition( self ):
    return self.__pos

  def moveLeft( self ):
    if self.__pos > CitBoard.MIN:
      self.__pos -= 1

  def moveRight( self ):
    if self.__pos < CitBoard.MAX:
      self.__pos += 1
# ------------------------------------
