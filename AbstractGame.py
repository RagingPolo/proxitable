from abc import ABCMeta, abstractmethod

# --------------------------------------------------------------------------- #
# CLASS AbstractGame
# Defines the required method of a Game to be called by the Game Launcher.
# Other private methods are allowed. Child class must be called main.py and
# be found in a sub directory of the Game launcher.
# Also requires a main.conf file to be present in the following 3 line format:
#   Line 1: Player one input module
#   Line 2: Player two input module
#   Line 3: Game output module 
#   Line format - <module name>:[args,...]
# A simlink to this abstract class file is also required in the games directory
# --------------------------------------------------------------------------- #
class AbstractGame( object ):
  __metaclass__ = ABCMeta

  # Should start the main game loop
  @abstractmethod
  def run( self ):
    pass
  
  # Set the games input module
  #  @player - Player ( P1 | P2 ) the input is for
  #  @input_ - The input module
  @abstractmethod
  def setInput( self, player, imod ):
    pass

  # Set the games output module
  @abstractmethod
  def setOutput( self, omod ):
    pass

  # Should call the output connect method
  #  @omod - The output module
  @abstractmethod
  def connect( self, addr ):
    pass

  # Returns the name of the game
  @abstractmethod
  def getName( self ):
    pass

  # Copy any resouces required by the game GUI to the wsserver resources folder
  def copyResources( self ):
    game = self.getName().lower()
    base = os.path.dirname( os.path.realpath( __file__ ) )
    wssDir  = os.path.join( base, 'wsserver', 'resources' )
    gameDir = os.path.join( base, game, 'resources' )
    resDir = []
    for f in os.listdir( gameDir + '/' ):
      path = os.path.join( gameDir, f )
      if os.path.isdir( path ):
        resDir.append( path ) 
    for d in resDir:
      folder = os.path.basename( os.path.normpath( d ) )
      wss = os.path.join( wssDir, folder )
      try
        os.mkdir( os.path.join( wss, game ) )
      except OSError:
        # Squash, means folder already exists
        pass
      for f in os.listdir( d ):
        shutil.copy2( os.path.join( d, f ), os.path.join( wss, game, f ) )
