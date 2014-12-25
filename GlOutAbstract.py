from abc import ABCMeta, abstractmethod

class GlOutAbstract( object ):
  __metaclass__ = ABCMeta

  # Send 'msg' to output device
  def send( self, msg ):
    pass 

  # Perform any cleanup required by output module
  def cleanup( self ):
    pass
