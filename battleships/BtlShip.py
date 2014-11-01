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

  def getDirection( self ):
    return self.__dir

  def getX( self ):
    return self.__x

  def getY( self ):
    return self.__y

  def getSize( self ):
    return self.__size

  # Set the position of the ship and the direction on the board
  # Is is assumed that this position fits within the current game
  # board, checking should be done in the calling class as BtlShip
  # has no notion of what a board is
  def setPosition( self, x, y, direction ):
    if direction in [ '^', '>' ]:
      self.__x   = int( x )
      self.__y   = int( y )
      self.__dir = direction

  # Set a section of the ship as hit
  def setHit( self, pos ):
    if pos < self.__size:
      self.__hits[ pos ] = 1

  # Check if the specified board position hit the ship
  # Does not care or know if position is repeated
  # It is up to class supplying the position to make
  # such checks
  def isHit( self, x, y ):
    if ( self.__x is not None and 
         self.__y is not None and
         self.__dir is not None ):
      # Vertical ship
      if self.__dir == '^':
        if ( self.__x == x and
             self.__y >= y and
             self.__y < ( y + self.__size ) ):
          # Update record of hits
          self.__hits[ y - self.__y ] = 1
          return True
      # Horizontal ship
      elif self.__dir == '>':
        if ( self.__y == y and
             self.__x >= x and
             self.__x < ( x + self.__size ) ):
          # Update record of hits
          self.__hits[ x - self.__x ] = 1
          return True
      return False

  # Check if the ship is sunk
  def isSunk( self ):
    if sum( self.__hits ) == self.__size:
      return True
    else:
      return False
# ------------------------------------
