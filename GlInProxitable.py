from GlInAbstract import GlInAbstract
from ProxitableSim import ProxitableSim
import RPi.GPIO as GPIO
from time import sleep

# Interface with the proxitable hardware and poll
# for button presses on request
class GlInProxitable( GlInAbstract ):

  PINS = [ 12, 23, 18, 21, 26, 7, 10, 15 ]

#  def __init__( self ):
#    self.pes = ProxitableSim()

  def __str__( self ):
    return self.getName()

  def getName( self ):
    return 'Game Launcher Proxitable Input Module'

  # Keep polling for a button until one is pressed
  def getButton( self ):
    pin = 0
    while pin == 0:
      for i in self.PINS:
        if GPIO.input( i ):
          pin = i
          break
      sleep( 0.1 )
      #pin = int( self.pes.getPin() )
    return pin

  def cleanup( self ):
    pass
    #self.pes.closeThreads()
