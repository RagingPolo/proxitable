import socket

# TODO write abstract class to inherit from + something to clean up the socket at the end
class GlOutWss( object ):

  def __init__( self, ip, port ):
    try:
      self.__sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
      self.__sock.connect( ( ip, port ) )
    # TODO log these errors to file
    except socket.error as e:
      print( 'Error connecting to output server: ' + e )
      self.__sock = None
    except Exception as e:
      print( 'Error: ' + e )
      self.__sock = None

  def send( self, msg ):
    if self.__sock is not None:
       self.__sock.send( msg )
