from abc import ABCMeta, abstractmethod

# --------------------------------------------------------------------------- #
# CLASS GlOutAbstract
# Abstract class for Game Launcher Ouput module. Defines required methods to
# be called by the launcher. Other private methods can be added.
# --------------------------------------------------------------------------- #
class GlOutAbstract( object ):
  __metaclass__ = ABCMeta

  # Return the name of the output module, used for logging
  @abstractmethod
  def getName( self ):
    return 'Game Launcher Abstract Output - Module name not defined'

  # Overiding the object.__str__() with module name
  def __str__( self ):
    return self.getName()

  # Send 'msg' to output device
  @abstractmethod
  def send( self, msg ):
    pass 

  # Perform any cleanup required by output module
  @abstractmethod
  def cleanup( self ):
    pass
