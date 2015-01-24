from abc import ABCMeta, abstractmethod

# --------------------------------------------------------------------------- #
# CLASS GlOutAbstract
# Abstract class for Game Launcher Ouput module. Defines required methods to
# be called by the launcher. Other private methods can be added.
# --------------------------------------------------------------------------- #
class GlOutAbstract( object ):
  __metaclass__ = ABCMeta

  # Return the name of the output module
  @abstractmethod
  def getName( self ):
    pass

  # Send 'msg' to output device
  @abstractmethod
  def send( self, msg ):
    pass 

  # Perform any cleanup required by output module
  @abstractmethod
  def cleanup( self ):
    pass
