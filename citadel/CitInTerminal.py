import CitInAbstract
import getpass
import numbers
# ---------------------------------------------------------------------------- #
# CLASS CitInTerminal
# 
# Gets a human players input from the terminal 
# ---------------------------------------------------------------------------- #
class CitInTerminal( CitInAbstract.CitInAbstract ):

  # Set up an instance of the input module
  #  @args - empty list (this allows for the use of the generic module loader)
  def __init__( self, args ):
    # Set as non ai input
    super().__init__( False )

  # Get the players next move
  #  @name    - name of player entering move
  #  @points  - players current points total
  #  @last    - opponents last move ( not used by this method )
  #  @returns - move ( positive integer no greater than points )
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
# ---------------------------------------------------------------------------- #
