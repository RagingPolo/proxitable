from GlInAbstract import GlInAbstract
import RPi.GPIO as GPIO
from time import sleep

# --------------------------------------------------------------------------- #
# CLASS GlInProcitable
# Interface with the hardware based Proxitable controller. Will check for input
# buttons on request
# --------------------------------------------------------------------------- #
class GlInProxitable( GlInAbstract ):

  # Relevent pins for input from the PES hardware
  PINS = [ 12, 23, 18, 21, 26, 7, 10, 15 ]

  # Define the name of the module
  def getName( self ):
    return 'Game Launcher Proxitable Input Module'

  # When a button press is requested keep polling the GPIO pins until one is
  # high signifying a button has been pressed
  def getButton( self ):
    pin = 0
    while pin == 0:
      for i in self.PINS:
        if GPIO.input( i ):
          pin = i
          break
      sleep( 0.1 )
    return pin

  # Stub as this module does not require any cleanup actions
  def cleanup( self ):
    pass
