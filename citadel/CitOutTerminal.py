import CitOutAbstract
from colorama import init, Fore
import os
# ------------------------------------
# CLASS CitOutTerminal               |
#                                    |
# Basic output class displaying the  |
# current game state on the command  |
# line                               |
# ------------------------------------
class CitOutTerminal( CitOutAbstract.CitOutAbstract ):

  # Args will be an empty list, to allow the use of
  # a generic dynamic module loader
  def __init__( self, args ):
    super().__init__()
    init() # Colorama init

  def showState( self, pos, p1p, p2p, p1m, p2m ):
    os.system( 'cls' if os.name == 'nt' else 'clear' ) 
    print( Fore.CYAN + '   P1[' + Fore.RED + '{0:2d}'.format( p1p ) + Fore.CYAN + ']' + Fore.WHITE +
           '-->         <--' + Fore.CYAN + '[' + Fore.RED + '{0:2d}'.format( p2p ) + Fore.CYAN + ']P2' )
    print( Fore.YELLOW + '                |' )
    print( '            | - | - |' )
    print( '        |- -|- -|- -|- -|' )
    if pos == 0:
      print( ' --[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 1:
      print( ' --[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 2:
      print( ' --[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 3:
      print( ' --[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]-[ ]--' )
    elif pos == 4:
      print( ' --[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]-[ ]--' )
    elif pos == 5:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']-[ ]--' )
    elif pos == 6:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW + ']--' )
    else:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    print( '        |- -|- -|- -|- -|' )
    print( '            | - | - |' )
    print( '                |' + Fore.RESET )
    print()

  def showResult( self, result ):
    if result == self.P1:
      print( Fore.WHITE + '         Player One Wins' + Fore.RESET )
    elif result == self.P2:
      print( Fore.WHITE + '         Player Two Wins' + Fore.RESET )
    elif result == self.DRAW:
      print( Fore.WHITE + '               Draw!' + Fore.RESET )
    print()
# ------------------------------------
