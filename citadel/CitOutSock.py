from CitOutAbstract import CitOutAbstract
import socket
import struct

class CitOutSock( CitOutAbstract ):

  def __init__( self, ip, port ):
    super().__init__()
    try:
      self.sock = socket.socket()
      self.sock.connect( ( str( ip ), int( port ) ) )
    except socket.error as e:
      print( 'Error connecting to output server: ' + e )
    except Exception as e:
      print( 'Error: ' + e )

  def showState( self, pos, p1p, p2p, p1m, p2m ):
    html = []
    html.append( '{"cmd":"R","tag":"#game","html":"' )
    html.append( '<p /><p /><center>' )
    html.append( '  <table border=\'1\'>' )
    html.append( '    <tr>' )
    html.append( '      <td>' + str( p1p ) + '</td>' )
    html.append( '      <td>' + str( pos ) + '</td>' )
    html.append( '      <td>' + str( p2p ) + '</td>' )
    html.append( '    </tr>' )
    html.append( '  </table>' )
    html.append( '</center>' )
    html.append( '"}' )
    self.__send( bytes( ''.join( html ), 'utf-8' ) )

  def showResult( self, result ):
    winner = ''
    if result == self.P1:
      winner = 'Player One Wins'
    elif result == self.P2:
      winner = 'Player Two Wins'
    elif result == self.DRAW:
      winner = 'Draw!'
    html = []
    html.append( '{"cmd":"R","tag":"#game","html":"' )
    html.append( '<p /><p /><center><b>Game Over: ' + winner + '</b></center>' )
    html.append( '"}' )
    self.__send( bytes( ''.join( html ), 'utf-8' ) )

  def __send( self, data ):
    size = struct.pack( '>I', len( data ) )
    self.sock.send( size + data )
# ------------------------------------
