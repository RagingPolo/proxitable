import os

# ------------------------------------
# CLASS Launcher
#
# Load input and output modules. Load
# available games, launch selected 
# game and support its IO when 
# requested. Regain execution when 
# game finishes
# ------------------------------------
class Launcher( object ):

  def __init__( self )
    self.imod  = None
    self.omod  = None
    self.games = self.__loadGames()

  def __loadGames( self ):
    games = []
    for d in os.walk( '.' ).__next__()[ 1 ]:
      if os.path.isfile( d + '/main.py' ):
        # TODO create abstract game class, make each 
        # game use a main.py that is a subclass
        # load game object into games array
        games.append( d + '/main.py' )
    return games

  # Using information from the games object generate
  # the load menu to be displayed to the user
  def genMenu( self ):
    pass

  def setInputMod( self, imod ):
    #if imod is of class abstrct imod
    self.imod = imod

  def setOutputMod( self, omod ):
    #if omod is of class abstract omod
    self.omod = omod
  
# ------------------------------------

if __name__ == '__main__':
  launch = Launcher()
