from BtlOutputAbstract import BtlOutputAbstract
from BtlPlayer import BtlPlayer
from BtlMove import BtlMove
from colorama import init, Fore
from string import ascii_uppercase
import os
# ------------------------------------
# CLASS BtlOutputTerminal            |
#                                    |
# Display the current game state for |
# a single player using ASCII art    |
# ------------------------------------
class BtlOutputTerminal( BtlOutputAbstract ):
  
  def __init__( self ):
    super().__init__()
    init() # Colorama init

  def showState( self, player, opponent ):
    os.system( 'cls' if os.name == 'nt' else 'clear' )
    size = player.getBoard().getSize()
    # Print X scales
    xscale = list( ascii_uppercase[ : size ] )
    print( '\n   ', end='' )
    for x in xscale:
      print( x + ' ', end='' )
    print( '      ', end='' )
    for x in xscale:
      print( x + ' ', end='' )
    print()
    # Print Y scale + a line from both boards
    for y in range( 0, size ):
      print( Fore.RESET + '{0:02d} '.format( y + 1 ), end='' )
      # Player board
      for x in range( 0, size ):
        # Display the ship or water
        water = True
        for ship in player.getBoard().getShips():
          # Check if it is an opponents shot
          pos = BtlMove.genMove( x, y ) 
          for shot in opponent.getMoveHistory():
            if shot == pos:
              if shot.wasHit() is True:
                print( Fore.RED + 'X ', end='' )    
              else:
                print( Fore.CYAN + 'O ', end='' )
              water = False
              break
          if water == False:
            break
          # if not is it an unhit bit of ship
          if ship.isHit( x, y, False ) is True:
            print( Fore.GREEN + 'X ', end='' )
            water = False
            break
        # Else it must be water
        if water is True:  
          print( Fore.BLUE + '~ ', end='' )
      # Opposition board
      print( Fore.RESET + '   {0:02d} '.format( y + 1 ), end='' )
      for x in range( 0, size ):
        water = True
        # Check if it is one of your shots
        pos = BtlMove.genMove( x, y ) 
        for shot in player.getMoveHistory():
          if shot == pos:
            if shot.wasHit() is True:
              print( Fore.RED + 'X ', end='' )    
            else:
              print( Fore.CYAN + 'O ', end='' )
            water = False
            break
        # Else it must be water
        if water is True:
          print( Fore.BLUE + '~ ', end='' )
      print()
    print( Fore.RESET )

  def displayWinner( self, player ):
    print( player.getName() + ' wins!' )
# ------------------------------------
