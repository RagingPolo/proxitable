from CitOutAbstract import CitOutAbstract
from colorama import init, Fore
import os
# ---------------------------------------------------------------------------- #
# CLASS CitOutTerminal
#
# Basic output class displaying the current game state on the command line.
# Requires the module colorama to be installed for coloured output
# ---------------------------------------------------------------------------- #
class CitOutTerminal( CitOutAbstract ):

  # Set up the class instance
  #  @args - empty list (this allows for the use of the generic module loader)
  def __init__( self, args ):
    super().__init__()
    init() # Colorama init

  # Stub method - not required by this output module
  def connect( self, addr ):
    pass

  # Display the game in it's starting state
  def newGame( self ):
    self.showState( 3, 50, 50, 0, 0 )

  # Display the current game state
  #  @pos - board position : 0-6 
  #  @p1p - player one points : 0-50
  #  @p2p - player two points : 0-50
  #  @p1m - player one last move : int
  #  @p2m - player two last move : int
  def showState( self, pos, p1p, p2p, p1m, p2m ):
    os.system( 'cls' if os.name == 'nt' else 'clear' ) 
    print( Fore.CYAN + '   P1[' + Fore.RED + '{0:2d}'.format( p1p ) + Fore.CYAN
           + ']' + Fore.WHITE + '-->         <--' + Fore.CYAN + '[' + Fore.RED +
                                    '{0:2d}'.format( p2p ) + Fore.CYAN + ']P2' )
    print( Fore.YELLOW + '                |' )
    print( '            | - | - |' )
    print( '        |- -|- -|- -|- -|' )
    if pos == 0:
      print( ' --[' + Fore.RED + 'x' + Fore.YELLOW +
                                                 ']-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 1:
      print( ' --[ ]-[' + Fore.RED + 'x' + Fore.YELLOW +
                                                     ']-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 2:
      print( ' --[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW +
                                                         ']-[ ]-[ ]-[ ]-[ ]--' )
    elif pos == 3:
      print( ' --[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW +
                                                             ']-[ ]-[ ]-[ ]--' )
    elif pos == 4:
      print( ' --[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW +
                                                                 ']-[ ]-[ ]--' )
    elif pos == 5:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW +
                                                                     ']-[ ]--' )
    elif pos == 6:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[' + Fore.RED + 'x' + Fore.YELLOW +
                                                                         ']--' )
    else:
      print( ' --[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]--' )
    print( '        |- -|- -|- -|- -|' )
    print( '            | - | - |' )
    print( '                |' + Fore.RESET )
    print()

  # Display the game result
  #  @result - the game result : P1, P2, DRAW
  def showResult( self, result ):
    if result == self.P1:
      print( Fore.WHITE + '         Player One Wins' + Fore.RESET )
    elif result == self.P2:
      print( Fore.WHITE + '         Player Two Wins' + Fore.RESET )
    elif result == self.DRAW:
      print( Fore.WHITE + '               Draw!' + Fore.RESET )
    print()
# ---------------------------------------------------------------------------- #
