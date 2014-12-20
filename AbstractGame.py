from abc import ABCMeta, abstractmethod

class AbstractGame( object ):
  __metaclass__ = ABCMeta

  @abstractmethod
  def run( self ):
    pass
  
  @abstractmethod
  def setInput( self, player, imod ):
    pass

  @abstractmethod
  def setOutput( self, omod ):
    pass

  @abstractmethod
  def getName( self ):
    pass
