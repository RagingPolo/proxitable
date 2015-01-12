import os
import sys
import threading
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
                  68 : 26, 97 : 7, 98 : 10, 115 : 15 }
    self.selected = 0
    thread = threading.Thread( target=self.__readInput, name='readButtons' )
    thread.start()    

  def __readInput( self ):
    self.fd = sys.stdin.fileno()
    self.old_settings = termios.tcgetattr( self.fd )
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

  def getPin( self ):
    selected = self.selected
    self.selected = 0
    return selected

  def closeThreads( self ):
    termios.tcsetattr( self.fd, termios.TCSADRAIN, self.old_settings )
    self.selected = -1
