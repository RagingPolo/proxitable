from abc import ABCMeta, abstractmethod

class GlOutAbstract( object ):
  __metaclass__ = ABCMeta

  # Return the name of the output module
  @abstractmethod
  def getName( self ):

  # Send 'msg' to output device
  @abstractmethod
  def send( self, msg ):
    pass 

  # Perform any cleanup required by output module
  @abstractmethod
  def cleanup( self ):
    pass
