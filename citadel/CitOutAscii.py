import CitOutAbstract
from colorama import init, Fore
import os

class CitOutAscii( CitOutAbstract ):

  def __init__( self ):
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
    pass
