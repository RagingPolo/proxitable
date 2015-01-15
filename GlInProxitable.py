from GlInAbstract import GlInAbstract
from ProxitableSim import ProxitableSim

# Interface with the proxitable hardware and poll
# for button presses on request
class GlInProxitable( GlInAbstract ):

  def __init__( self ):
    self.pes = ProxitableSim()

  def __str__( self ):
    return self.getName()

  def getName( self ):
    return 'Game Launcher Proxitable Input Module'

  # Keep polling for a button until one is pressed
  def getButton( self ):
    pin = 0
    while pin == 0:
      pin = int( self.pes.getPin() )
    return pin

  def cleanup( self ):
    self.pes.closeThreads()
