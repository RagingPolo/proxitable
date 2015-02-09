from GlInAbstract import GlInAbstract
from time import sleep
from testCode.ProxitableSim import ProxitableSim 

# --------------------------------------------------------------------------- #
# CLASS GlInKeyboard
# Interface with a keyboard. Will check for input
# buttons on request
# --------------------------------------------------------------------------- #
class GlInKeyboard( GlInAbstract ):

  # Relevent pins for input from the PES hardware
  PINS = [ 12, 23, 18, 21, 26, 7, 10, 15 ]
  def __init__( self ):
     self.pSim = ProxitableSim()
  # Define the name of the module
  def getName( self ):
    return 'Game Launcher Keyboard Input Module'

  # When a button press is requested keep polling the GPIO pins until one is
  # high signifying a button has been pressed
  def getButton( self ):
    pin = 0
    while pin == 0:
      pin = self.pSim.getPin()
      sleep(0.1)
    return pin

  # Stub as this module does not require any cleanup actions
  def cleanup( self ):
    pass
