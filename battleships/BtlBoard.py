from BtlShip import BtlShip
from BtlMove import BtlMove
import random
from os import urandom
# ------------------------------------
# CLASS BtlBoard                     |
#                                    |
# Maintain the state of a single     |
# board                              |
# ------------------------------------
class BtlBoard( object ):

  # Create a board, size 6 or 7 - 3 ships
  #                 size 8 to 9 - 4 ships
  #                 size 10     - 5 ships
  def __init__( self, size ):
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
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
      self.__ships.append( BtlShip( 'Submarine', 3 ) )
    if size == 10:
      self.__ships.append( BtlShip( 'Aircraft Carrier', 5 ) )
    # Create board matrix
    self.__board = [ [ 0 for x in range( size ) ] for x in range( size ) ]
    self.__size = size

  def getSize( self ):
    return self.__size

  def getShips( self ):
    return self.__ships

  # Check if all of the ships on the board have been sunk
  def isAllSunk( self ):
    for ship in self.__ships:
      if ship.isSunk is False:
        return False
    return True
  
  # Check a players move against the ships
  # on the board.
  # Returns True if a hit
  #         False if a miss
  def takeShot( self, move ):
    if isinstance( move, BtlMove ):
      for ship in self.__ships:
        if ship.isHit( move.getX(), move.getY(), True ) is True:
          return True
      return False
    else:
      raise TypeError( 'BtlBoard().takeShot() - Not a valid move object' )

  # Randomly position the availible ships on the board
  def positionShips( self ):
    overlap = True
    # Repeat until no ships overlap
    while overlap is True:
      # Pick some random positions
      for ship in self.__ships:
        onboard = False
        while onboard is False:
          x = random.randrange( 0, self.__size - 1 )
          y = random.randrange( 0, self.__size - 1 )
          d = direction = random.choice( 'v>' )
          if d == 'v':
            onboard = ( y + ship.getSize() - 1 ) < self.__size
          else: # d == '>'
            onboard = ( x + ship.getSize() - 1 ) < self.__size
        ship.setPosition( x, y, d )    
      # Check that they don't overlap
      # TODO Could this be altered sensibly to make sure they don't touch either
      overlap = False
      for ship in self.__ships:
        if overlap is True: break
        for boat in self.__ships:
          if overlap is True: break
          if ship is not boat:
            if ship.getDirection() == 'v':
              x = ship.getX()
              for y in range( ship.getY(), ship.getY() + ship.getSize() ):
                overlap = boat.isHit( x, y, False )
                if overlap is True: break
            else: # direction is '>'
              y = ship.getY()
              for x in range( ship.getX(), ship.getX() + ship.getSize() ):
                overlap = boat.isHit( x, y, False )
                if overlap is True: break
