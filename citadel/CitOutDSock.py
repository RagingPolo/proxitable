from CitOutAbstract import CitOutAbstract
import socket
import struct

class CitOutDSock( CitOutAbstract ):

  CSS = '.display { background-color: #0000AF; color: #FFF; vertical-align: middle; float: left; -webkit-border-radius: 1%; -moz-border-radius: 1%; border-radius: 10px; }
.player-display { margin: 1% 10% 1% 10%; height: 80%; width: 30%; }
.position-display { margin: 1% 1% 1% 1%; height: 50px; width: 12%; }
.container { width: 80%; margin: 0.5% auto; overflow: hidden; }
.player-container { height: 30%; }'
  HTML = '<div class="container player-container">
  <div id="player_one" class="display player-display">
    <h1 id="p2_name">Player One</h1>
    <h2 id="p1_points">50</h2>
  </div>
  <div id="player_two" class="display player-display">
    <h1 id="p2_name">Player Two</h1>
    <h2 id="p2_points">50</h2>
  </div>
</div>
<br />
<div class="container">
  <div id="pos0" class="display position-display"></div>
  <div id="pos1" class="display position-display"></div>
  <div id="pos2" class="display position-display"></div>
  <div id="pos3" class="display position-display"></div>
  <div id="pos4" class="display position-display"></div>
  <div id="pos5" class="display position-display"></div>
  <div id="pos6" class="display position-display"></div>
</div>'

  def __init__( self ):
    super().__init__()
    self.__sock = None

  def connect( self, addr )
    try:
      self.__sock = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
      self.__sock.connect( addr )
      return True
    # TODO log these errors to file
    except socket.error as e:
      print( 'Error connecting to output server: ' + e )
    except Exception as e:
      print( 'Error: ' + e )
    return False

  def newGame( self ):
    self.__send( self.__genJsonBytes( 'R', '#game-css', self.CSS ) )
    self.__send( self.__genJsonBytes( 'R', '#game-html', self.HTML ) )

  def showState( self, pos, p1p, p2p, p1m, p2m ):
    self.__send( self.__genJsonBytes( 'R', '#p1_points', str( p1p ) ) )    
    self.__send( self.__genJsonBytes( 'R', '#p2_points', str( p2p ) ) )
    self.__send( self.__getJsonBytes( 'X', 'None', '$( ".position-display" ).css( "background-color", "#0000AF" );' )
    self.__send( self.__getJsonBytes( 'X', 'None', '$( "#pos' + str( pos ) + '" ).css( "background-color", "#FFF" );' )

  def showResult( self, result ):
    winner = ''
    if result == self.P1:
      winner = 'Player One Wins'
    elif result == self.P2:
      winner = 'Player Two Wins'
    elif result == self.DRAW:
      winner = 'Draw!'
    self.__send( self.__genJsonBytes( 'R', '#game-io', '<center><b>Game Over: ' + winner + '</b></center>' ) )

  def __genJsonBytes( self, cmd, target, content ):
    return bytes( '{"cmd":"' + cmd + '","target":"' + target + '","content":"' + content + '"}', 'utf-8' )

  def __send( self, data ):
    if self.__sock is not None:
      size = struct.pack( '>I', len( data ) )
      self.__sock.send( size + data )
# ------------------------------------
