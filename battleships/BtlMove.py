# ------------------------------------
# CLASS BtlMove                      |
#                                    |
# Stores a single move and           |
# translates between human           |
# coordinates, A1, and list indexes, |
# 00.                                |
# ------------------------------------
class BtlMove( object ):

  X = { 'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9 }

  def __init__( self, x, y ):
    if ( str( x ).upper() in [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J' ] and
         int( y ) in range( 1, 11 ) ):
      self.__x = x
      self.__y = y
      self.__hit = False
    else:
      raise TypeError( 'BtlMove() - invalid move' )
 
  # Convert numeric positions into a move object
  # ie 0,0 into BtlMove( A, 1 )
  @staticmethod
  def genMove( x, y ):
    if int( x ) in range( 0, 10 ) and int( y ) in range( 0, 10 ):
      xx = [ key for key, value in BtlMove.X.items() if value == x ][0]
      return BtlMove( xx, y + 1 )
    else: 
      raise Exception( 'BtlMove.genMove() - position out of range' )

  def setHit( self, hit ):
    if hit is True:
      self.__hit = True
    else:
      self.__hit = False

  def wasHit( self ):
    return self.__hit is True

  # Returns a tuple containing the move as list indexes
  def getMove( self ):
    return ( BtlMove.X[ self.__x ], self.__y - 1 )

  def getX( self ):
    return BtlMove.X[ self.__x ]

  def getY( self ):
    return self.__y - 1

  def __str__( self ):
    return self.__x + str( self.__y )

  def __eq__( self, other ):
    return self.getX() == other.getX() and self.getY() == other.getY()

  def __ne__( self, other ):
    return self.getX() != other.getX() and self.getY() != other.getY()
  
  def __gt__( self, other ):
    if self.getY() == other.selfY():
      return self.getX() > other.getX()
    else:
      return self.getY() > other.getY()

  def __lt__( self, other ):
    if self.getY() == other.getY():
      return self.getX() < other.getX()
    else:
      return self.getY() < other.getY()
  
  def __ge__( self, other ):
    if self.getY() == other.selfY():
      return self.getX() >= other.getX()
    else:
      return self.getY() >= other.getY()

  def __le__( self, other ):
    if self.getY() == other.getY():
      return self.getX() <= other.getX()
    else:
      return self.getY() <= other.getY()
# ------------------------------------
