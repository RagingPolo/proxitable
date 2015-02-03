#!/opt/python3.4/bin/python3.4
import sys
import struct
import socket
import logging
import socketserver
from io import StringIO
from hashlib import sha1
from binascii import a2b_hex
from base64 import b64encode
from email import message_from_string

# --------------------------------------------------------------------------- #
# CLASS wsserver
#
# Accepts websocket connections from a browser and act as an intermediary
# between the game launcher and the browser.
# --------------------------------------------------------------------------- #
class wsserver( socketserver.StreamRequestHandler ):

  # GUID as described in RFC 6455
  GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
  # Port to listen for connections from the game launcher on 
  PORT = 9000
 
  # Called before the server is started, sets up server specific logging and
  # class atrributes
  def setup( self ):
    # Setup logging
    LOGFORMAT = ( '[ %(levelname)s ] [ %(asctime)-15s ] '
                  '[ %(module)s.%(funcName)s() ] [ %(message)s ]' )
    logging.basicConfig( filename='.wsserver.log', level=logging.INFO,
                                                              format=LOGFORMAT )
    logging.info( 'Wsserver started' )
    # Setup server
    socketserver.StreamRequestHandler.setup( self )
    self.handshake = False # Has the web socket handshake happened yet
    self.lsock     = False # Socket for listening to connections from games
    self.gsock     = False # Active socket for a connected game

  # Main loop once server is up and running. Output modules can pass msgs to
  # the server using a local socket connection and the server forward them on
  # to the client browser
  def handle( self ):
    while True:
      if self.lsock is False:
        # Setup listening socket for recieveing game output
        self.lsock = socket.socket()
        try:
          self.lsock.bind( ( '', self.PORT ) )
          self.lsock.listen( 1 )
          logging.info( 'Wsserver listening for game connection on port %d', self.PORT )
        except socket.error as e:
          logging.execption( 'Wsserver startup failed' )
          self.lsock.close()
          sys.exit( 1 )
      elif self.handshake is False:
        self.doHandshake()
      else:
        if self.gsock is False:
          try:
            self.gsock = self.lsock.accept()[ 0 ]
          except socket.error as e:
            logging.exception( 'Error accpeting connectiob from game' )
        else:
          # Wait for data from output modules to pass onto client
          # Incomming messages in format of:
          # [ size ][ data ] size os 4 bytes big endian, data is of size bytes
          size = self.gsock.recv( 4 )
          if len( size ) > 0:
            size = struct.unpack( '>I', size )[ 0 ]
            data = self.gsock.recv( size )  
            self.sendMsg( data )
          else:
            self.gsock.close()
            self.gsock = False
            logging.info( 'Game connection closed' )

  # Complete handshake with client as per rfc6455
  def doHandshake( self ):
    data = self.request.recv( 1024 ).strip()
    stream = StringIO()
    rxString = data.decode( 'utf-8' ).split( '\r\n', 1 )[ 1 ]
    stream.write( rxString )  
    hdrs = message_from_string( rxString )
    print( hdrs ) 
    if hdrs.get( 'Upgrade', None ) == 'websocket':
      # Generate Sec-WebSocket-Accept value
      digest = bytes( hdrs[ 'Sec-WebSocket-Key' ] + self.GUID , 'utf-8' )
      digest = a2b_hex( bytes( sha1( digest ).hexdigest(), 'utf-8' ) )
      digest = str( b64encode( digest ) )[ 2 : -1 ]
      # Generate and send handshake response
      response = []
      response.append( 'HTTP/1.1 101 Switching Protocols\r\n' )
      response.append( 'Connection: Upgrade\r\n' )
      response.append( 'Upgrade: websocket\r\n' )
      response.append( 'Sec-WebSocket-Accept: ' + digest + '\r\n\r\n' )
      response = ''.join( response )
      print( response )
      self.handshake = self.request.send( bytes( response, 'utf-8' ) )
      logging.info( 'web socket connect established using client key: %s',
                                                   hdrs[ 'Sec-WebSocket-Key' ] )

  # Construct a message with preceeded by size and pass it on to the browser
  def sendMsg( self, msg ):
    if isinstance( msg, str ):
      msg = bytes( msg, 'utf-8' )
    length = len( msg )
    if length <= 125:
      hdr = struct.pack( '>BB', 129, length )
    elif length >= 126 and length <= 65535:
      hdr = struct.pack( '>BBH', 129, 126, length )
    else:
      hdr = struct.pack( '>BBQ', 129, 127, length )
    self.request.send( hdr + msg )
    logging.debug( 'Msg sent' )

# Start the server and serve indefinitely
if __name__ == '__main__':
  server = socketserver.TCPServer( ( 'localhost', 8000 ), wsserver )
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    server.server_close();
