#!/usr/bin/env python3
import os
import sys
import importlib.machinery
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
    # Test code
    for x in self.games:
      x.run()

  def __loadGames( self ):
    games = []
    for d in os.walk( '.' ).__next__()[ 1 ]:
      if ( os.path.isfile( d + '/main.py' ) and
           os.path.isfile( d + '/main.conf' ) ):
        try:
          # Add game folder to the python path and load the main module
          sys.path.append( os.path.abspath( d ) )
          mod = importlib.machinery.SourceFileLoader( 'Main', d + '/main.py' ).load_module()
          game = mod.Main()
          # Set up input and output from config file
          with open( d + '/main.conf' ) as ioConf:
            # main.conf file specifys the io modules to be loaded for the game
            # the file should consist of three lines
            # Line 1: Player one input module
            # Line 2: Player two input module
            # Line 3: Game output module 
            # Line format - <module name>:[args,...]
            game.setInput( 1, self.__setupIOModule( ioConf.readline() ) )
            game.setInput( 2, self.__setupIOModule( ioConf.readline() ) )
            game.setOutput( self.__setupIOModule( ioConf.readline() ) )
          games.append( game )
        except Exception as e:
          # TODO log the error to a proper log file
          print( e )
    return games

  # Load specified io module and instantiate with givern args
  def __setupIOModule( self, line ):
    io = line.rstrip().split( ':' )
    if len( io ) > 1:
      ioClass = self.__importClass( io[ 0 ] )
      if len( io[ 1 ][ 1 : -1 ] ) > 0:
        args = io[ 1 ][ 1 : -1 ].split( ',' )
      else:
        args = []
      return ioClass( args )
    return None

  # Return a callable object from the imported module
  def __importClass( self, name ):
    mod = importlib.import_module( name )
    return getattr( mod, name )

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
