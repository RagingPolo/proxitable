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
    pass
 
  # return a pin number representing a button
  @abstractmethod
  def getButton( self ):
    pass

  # Perform any cleanup required for the input module
  @abstractmethod
  def cleanup( self ):
    pass
