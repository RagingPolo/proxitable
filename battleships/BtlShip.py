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
    if direction in [ 'v', '>' ]:
      self.__x   = int( x )
      self.__y   = int( y )
      self.__dir = direction

  # Set a section of the ship as hit
  def setHit( self, pos ):
    if pos < self.__size:
      self.__hits[ pos ] = 1

  # Check if part of the ship is at x,y position
  # If shot is True it is record as an actual hit on the ship
  # Does not care or know if position is repeated
  # It is up to class supplying the position to make
  # such checks
  def isHit( self, x, y, shot ):
    if ( self.__x is not None and 
         self.__y is not None and
         self.__dir is not None ):
      # Vertical ship
      if self.__dir == 'v' and self.__x == x:
         if y >= self.__y and y < ( self.__y + self.__size ):
          if shot is True:
            self.__hits[ self.__y - y ] = 1
          return True
      # Horizontal ship
      elif self.__dir == '>' and self.__y == y:
        if x >= self.__x and x < ( self.__x + self.__size ):
          if shot is True:
            self.__hits[ self.__x - x ] = 1
          return True
    return False

  # Check if the ship is sunk
  def isSunk( self ):
    if sum( self.__hits ) == self.__size:
      return True
    else:
      return False
# ------------------------------------
