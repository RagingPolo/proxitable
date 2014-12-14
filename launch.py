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

  def __init__( self ):
    self.imod  = None
    self.omod  = None
    self.games = self.__loadGames()

  def __loadGames( self ):
    games = []
    dirs = os.walk( '.' ).next()[ 1 ]
    for d in dirs:
      print( d )
    #list all folders in cwd
    #if they contain a main.py file add to list
    return games

  def setInputMod( self, imod ):
    #if imod is of class abstrct imod
    self.imod = imod

  def setOutputMod( self, omod ):
    #if omod is of class abstract omod
    self.omod = omod  
  
# ------------------------------------
