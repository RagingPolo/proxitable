from GlOutAbstract import GlOutAbstract
import socket
import logging

class GlOutWss( GlOutAbstract ):

  def __init__( self, ip, port ):
    try:
      self.__sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
      self.__sock.connect( ( ip, port ) )
    except socket.error as e:
      logging.exception( 'Error connectiong to output server' )
      self.__sock = None

  def getName( self ):
    return 'Game Launcher Web Socket Server Output Module'

  def __str__( self ):
    return self.getName()

  def send( self, msg ):
    if self.__sock is not None:
       self.__sock.send( msg )
    else:
      logging.warning( 'No socket to send data' )

  def cleanup( self ):
    if self.__sock is not None:
      self.__sock.close()
    else:
      logging.warning( 'No socket to close' )
