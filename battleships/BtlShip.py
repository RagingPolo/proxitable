import numbers
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
    self.__x    = None
    self.__y    = None
    self.__dir  = None

  def getName( self ):
    return self.__name

  # Set the position of the ship and the direction on the board
  def setPosition( self, x, y, direction ):
    if ( direction in [ '^', '>' ] and
         isinstance( x, numbers.Number ) and
         isinstance( y, numbers.Number ) ):
      self.__x   = x
      self.__y   = y
      self.__dir = direction
    else:
      raise Exception( 'BtlShip.setPosition() - Invalid position' )

  # Set a section of the ship as hit
  def setHit( self, pos ):
    if pos < self.__size:
      self.__hits[ pos ] = 1

  # Check if the specified board position hit the ship
  def isHit( self, x, y ):
    if self.__dir == '^':
      if ( self.__x == x and
           self.__y >= y and
           self.__y < ( y + self.__size ) ):
        return True
    elif self.__dir == '>':
      if ( self.__y == y and
           self.__x >= x and
           self.__x < ( x + self.__size ) ):
        return True
    return False

  # Check if the ship is sunk
  def isSunk( self ):
    if sum( self.__hits ) == self.__size:
      return True
    else:
      return False
# ------------------------------------
