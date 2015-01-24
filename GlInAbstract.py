from abc import ABCMeta, abstractmethod
  
# --------------------------------------------------------------------------- #
# CLASS GlInAbstract
# Abstract class for Game Launcher Input module. Defines required methods to
# be called by the launcher. Other private methods can be added.
# --------------------------------------------------------------------------- #
class GlInAbstract( object ):
  __metaclass__ = ABCMeta

  # Return the name of the module for logging
  @abstractmethod
  def getName( self ):
    return 'Game Launcher Abstract Input - Module name not defined'
 
  # Overiding the object.__str__() with module name
  def __str__( self ):
    return self.getName()
  
  # return a pin number representing a button
  @abstractmethod
  def getButton( self ):
    pass

  # Perform any cleanup required for the input module
  @abstractmethod
  def cleanup( self ):
    pass
