import struct
import socketserver
from base64 import b64encode
from hashlib import sha1
from email import message_from_string
from io import StringIO
from binascii import a2b_hex
import socket
from sys import exit

class wsserver( socketserver.StreamRequestHandler ):

  GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
 
  def setup( self ):
    socketserver.StreamRequestHandler.setup( self )
    self.handshake = False
    self.lsock     = False
    self.gsock     = False

  # Main loop once server is up and running
  # Output modules can pass msgs to the server
  # using a local socket connection and the server 
  # forward them on to the client browser
  def handle( self ):
    while True:
      if self.lsock is False:
        print( 'Hello' )
        # Setup listening socket for recieveing game output
        self.lsock = socket.socket()
        try:
          self.lsock.bind( ( '', 9000 ) )
          self.lsock.listen( 1 )
        except socket.error as e:
          print( 'wsserver startup failed: ' + e )
          self.lsock.close()
          exit( 1 )
      elif self.handshake is False:
        self.doHandshake()
      else:
        if self.gsock is False:
          self.gsock = self.lsock.accept()[ 0 ]
        else:
          # Wait for data from output modules to pass onto client
          # Incomming messages in format of:
          # [ size ][ data ] size os 4 bytes big endian, data is of size bytes
          # TODO This is currently very naive and will crap out on any error
          size = self.gsock.recv( 4 )
          if len( size ) > 0:
            size = struct.unpack( '>I', size )[ 0 ]
            data = self.gsock.recv( size )  
            self.sendMsg( data )
          else:
            self.gsock.close()
            self.gsock = False

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
 
  def sendMsg( self, msg ):
    if isinstance( msg, str ):
      msg = bytes( msg, 'utf-8' )
    self.request.send( struct.pack( '>B', 129 ) )
    length = len( msg )
    if length <= 125:
      self.request.send( struct.pack( '>B', length ) )
    elif length >= 126 and length <= 65535:
      self.request.send( 126 )
      self.request.send( struct.pack( '>H', length ) )
    else:
      self.request.send( 127 )
      self.request.send( struct.pack( '>Q', length ) )
    self.request.send( msg )    

if __name__ == '__main__':
  server = socketserver.TCPServer( ( 'localhost', 8000 ), wsserver )
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    server.server_close();
