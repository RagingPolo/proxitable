import BtlShip
import random
from os import urandom
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
    # Initialise the random number generator
    random.seed( urandom( 128 ) )
    # Adjust size if needed
    if size < 6:
      size = 6
    elif size > 10:
      size = 10
    # Create ships
    self.__ships = [ BtlShip.BtlShip( 'Battleship', 4 ),
                     BtlShip.BtlShip( 'Destroyer', 3 ),
                     BtlShip.BtlShip( 'Gunship', 2 ) ]
    # Add more ships if needed 
    if size > 7:
      self.__ships.append( BtlShip.BtlShip( 'Submarine', 3 ) )
    if size == 10:
      self.__ships.append( BtlShip.BtlShip( 'Aircraft Carrier', 5 ) )
    # Create board matrix
    self.__board = [ [ 0 for x in range( size ) ] for x in range( size ) ]
    self.__size = size

  # Check if all of the ships on the board have been sunk
  def isAllSunk( self ):
    for ship in self.__ships:
      if ship.isSunk is False:
        return False
    return True

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

  # For testing ship positions before output modules have been written
  def testPrintBoard( self ):
    # Testing print out of the board
    for s in self.__ships:
      print( '   ' + s.getName()[ 0 : 1 ], s.getDirection(), s.getX(), s.getY(), s.getSize() )
    x = 0
    y = 0
    print( '\n  ', end='' )
    for i in range( 0, self.__size ):
      print( str( i ) + ' ', end='' )
    print()
    while y < self.__size:
      print( str( y ) + ' ', end='' )
      while x < self.__size:
        for ship in self.__ships:
          water = True
          if ship.isHit( x, y, False ) is True:
            print( ship.getName()[0:1] + ' ', end='' )
            water = False
            break
        if water is True:
          print( '~ ', end='' )
        x += 1
      x = 0
      y += 1
      print()

  # XXX What should this return to the main game class?
  # and what info can be retrieved by polling the board
  # XXX Actually should it even be in this class? Would 
  # it not be better in the player class and the player
  # class to have a board object??
  def takeShot( self, shot ):
    pass

# Testing of class
b = BtlBoard( 10 )
b.positionShips()
b.testPrintBoard()
