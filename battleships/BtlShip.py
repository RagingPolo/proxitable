# ------------------------------------
# CLASS BtlShip                      |
#                                    |
# Maintain state of an individual    |
# ship                               |
# ------------------------------------
class BtlShip( object ):

  def __init__( self, name, size ):
    self.__name = str( name )
    self.__size = int( size )
    self.__hits = [ 0 ] * self.__size

  def getName( self ):
    return self.__name

  # Set a section of the ship as hit
  def setHit( self, pos ):
    if pos < self.__size:
      self.__hits[ pos ] = 1

  # Check if the ship is sunk
  def isSunk( self ):
    if sum( self.__hits ) == self.__size:
      return True
    else:
      return False
# ------------------------------------
