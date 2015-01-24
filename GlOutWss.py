from GlOutAbstract import GlOutAbstract
import socket
import logging

# --------------------------------------------------------------------------- #
# CLASS GlOutWss
# Child class of the Game Launcher Abstract Output module
# Supports connection to the Web Socket Server, which in turn will push the 
# output to a browser.
# --------------------------------------------------------------------------- #
class GlOutWss( GlOutAbstract ):

  # When the module is loaded attempt to setup the connection to the Web Socket
  # Server. Failures will be recorded in the game launcher log
  def __init__( self, ip, port ):
    try:
      self.__sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
      self.__sock.connect( ( ip, port ) )
    except socket.error as e:
      logging.exception( 'Error connectiong to output server' )
      self.__sock = None

  # Returns the human readable name of the module
  def getName( self ):
    return 'Game Launcher Web Socket Server Output Module'

  # Send a 'msg' to the Web Socket Server
  def send( self, msg ):
    if self.__sock is not None:
       self.__sock.send( msg )
    else:
      logging.warning( 'No socket to send data' )

  # Perform the required cleanup actions - closing the socket if open
  def cleanup( self ):
    if self.__sock is not None:
      self.__sock.close()
    else:
      logging.warning( 'No socket to close' )
