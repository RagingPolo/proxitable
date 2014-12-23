from abc import ABCMeta, abstractmethod

class AbstractGame( object ):
  __metaclass__ = ABCMeta

  # Should start the main game loop
  @abstractmethod
  def run( self ):
    pass
  
  # Set the games input module
  @abstractmethod
  def setInput( self, player, imod ):
    pass

  # Set the games output module
  @abstractmethod
  def setOutput( self, omod ):
    pass

  # Should call the output connect method
  @abstractmethod
  def connect( self, addr ):
    pass

  # Returns the name of the game
  @abstractmethod
  def getName( self ):
    pass
