import BtlShip
# ------------------------------------
# CLASS BtlBoard                     |
#                                    |
# Maintain the state of a single     |
# board                              |
# ------------------------------------
class BtlBoard( object ):

  # Look up tables to convert A1 style coordinates into list indexes
  X = { 'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9 }
  # Would this would be better as just y - 1 ???
  Y = { 1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 0:9 }

  # Create a board, size 6 or 7 - 3 ships
  #                 size 8 to 9 - 4 ships
  #                 size 10     - 5 ships
  def __init__( self, size ):
    # Adjust size if needed
    if size < 6:
      size = 6
    elif size > 10:
      size = 10
    # Create ships
    self.__ships = [ BtlShip( 'Battleship', 4 ),
                     BtlShip( 'Destroyer', 3 ),
                     BtlShip( 'Gunship', 2 ) ]
    # Add more ships if needed 
    if size > 7:
      self.__ships.append( BtlShip( 'Submarine', 3 )
    if size == 10:
      self.__ships.append( BtlShip( 'Aircraft Carrier', 5 )
    # Create board matrix
    self.__board = [ [ 0 for x in range( size ) ] for x in range( size ) ]

  # Check if all of the ships on the board have been sunk
  def isAllSunk( self ):
    for ship in self.__ships:
      if ship.isSunk is False:
        return False
    return True

  # XXX Randomly position the availible ships on the board
  def positionShips( self ):
    pass

  # XXX What should this return to the main game class?
  # and what info can be retrieved by polling the board
  def takeShot( self, shot ):
    pass

