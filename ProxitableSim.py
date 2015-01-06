import os
import sys
import thread
import tty
import time
import termios

# key 13  enter : pin 12 start
# key 65  up    : pin 23 up
# key 66  down  : pin 18 down
# key 67  right : pin 21 right
# key 68  left  : pin 26 left
# key 97  a     : pin 07 a
# key 98  b     : pin 10 b
# key 115 s     : pin 15 select

class ProxitableSim( object ):

  def __init__( self ):
    self.pins = { 13 : 12, 65 : 23, 66 : 18, 67 : 21,
                  68 : 26, 97 : 07, 98 : 10, 115 : 15 }
    self.selected = 0
    thread.start_new_thread( self.__readInput, () )

  def __readInput( self ):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr( fd )
    try:
      tty.setraw( sys.stdin.fileno() )
      while True:
        if self.selected >= 0:
          key = ord( sys.stdin.read( 1 ) )
          if key == 27:
            sys.stdin.read( 1 )
            key = ord( sys.stdin.read( 1 ) )
            if key in self.pins.keys():
              self.selected = self.pins[ key ]
          else:
            if key in self.pins.keys():
              self.selected = self.pins[ key ]
        else:
          break
    finally:
      termios.tcsetattr( fd, termios.TCSADRAIN, old_settings )

  def getPin( self ):
    selected = self.selected
    self.selected = 0
    return selected

  def closeThreads( self ):
    self.selected = -1

if __name__ == '__main__':
  prox = ProxitableSim()
  for i in range( 10 ):
    time.sleep( 1 )
    pin = prox.getPin()
    if pin > 0:
      print chr( 27 ) + '[0G' + str( pin )
  prox.closeThreads() 
