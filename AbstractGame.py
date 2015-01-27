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
