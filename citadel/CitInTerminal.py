import CitInAbstract
import getpass
import numbers
# ------------------------------------
# CLASS CitInTerminal                |
#                                    |
# Class accepts and validates a      |
# players move from the terminal     |
# ------------------------------------
class CitInTerminal( CitInAbstract.CitInAbstract ):

  def getMove( self, name, points, last=None ):
    valid = False
    while valid is False:
      move = getpass.getpass( str( name ) + ' enter move: ' )
      try:
        move = int( move )
        if move > 0 and move <= points:
          valid = True
      except:
        valid = False
    return move
# ------------------------------------
