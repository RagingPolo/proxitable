# ------------------------------------
# CLASS BtlMove                      |
#                                    |
# Stores a single move and           |
# translates between human           |
# coordinates, A1, and list indexes, |
# 00. Imutable                       |
# ------------------------------------
class BtlMove( object ):

  X = { 'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9 }

  def __init__( self, x, y ):
    if ( str( x ).upper() in [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J' ] and
         int( y ) in range( 1, 11 ) ):
      self.__x = x
      self.__y = y
    else:
      raise TypeError( 'BtlMove() - invalid move' )

  # Returns a tuple containing the move as list indexes
  def getMoveIndex( self ):
    return ( BtlMove.X[ x ], y - 1 )

  # Returns a tuple containing the move as human readable strings
  def getMoveHuman( self ):
    return ( str( self.__x ), str( self.__y ) )
# ------------------------------------
