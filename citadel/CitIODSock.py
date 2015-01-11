from CitOutAbstract import CitOutAbstract
from CitInAbstract import CitInAbstract
import socket
import struct
import json
import logging

class CitOutDSock( CitInAbstract, CitOutAbstract ):

  CSS = """.display { background-color: #0000AF; color: #FFF; vertical-align: middle; float: left; -webkit-border-radius: 1%; -moz-border-radius: 1%; border-radius: 10px; }
.player-display { margin: 1% 10% 1% 10%; height: 80%; width: 30%; }
.position-display { margin: 1% 1% 1% 1%; height: 50px; width: 12%; }
.container { width: 80%; margin: 0.5% auto; overflow: hidden; }
.player-container { height: 30%; }"""
  HTML = """<div class="container player-container">
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
</div>"""
  MOVE = """<h1 id="move"></h1>"""
  # args is an empty list to support the dynamic module loader
  def __init__( self, args ):
    super().__init__()
    self.__sock = None
    self.ai = False
    self.points = 50

  def connect( self, addr ):
    try:
      self.__sock = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
      self.__sock.connect( addr )
      return True
    except socket.error as e:
      logging.exception( 'Failed to connect to game launcher' )
    except Exception as e:
      logging.exception( 'Connection error' )
    return False

  def newGame( self ):
    self.__send( self.__genJsonBytes( 'R', '#game-css', self.CSS ) )
    self.__send( self.__genJsonBytes( 'R', '#game-html', self.HTML ) )
    self.__send( self.__genJsonBytes( 'R', '#game-io', '' ) )

  # Send the current game state to the wssocket server
  def showState( self, pos, p1p, p2p, p1m, p2m ):
    self.__send( self.__genJsonBytes( 'R', '#p1_points', str( p1p ) ) )    
    self.__send( self.__genJsonBytes( 'R', '#p2_points', str( p2p ) ) )
    self.__send( self.__genJsonBytes( 'X', 'None', '$( ".position-display" ).css( "background-color", "#0000AF" );' ) )
    self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos' + str( pos ) + '" ).css( "background-color", "#000" );' ) )

  # Send the result to the wssocket server
  def showResult( self, result ):
    winner = ''
    if result == self.P1:
      winner = 'Player One Wins'
    elif result == self.P2:
      winner = 'Player Two Wins'
    elif result == self.DRAW:
      winner = 'Draw!'
    self.__send( self.__genJsonBytes( 'R', '#game-io', '<center><b>Game Over: ' + winner + '</b></center>' ) )

  # Listen for input from the proxitable
  def getMove( self, name, points, last ):
    move = self.points
    self.__send( self.__genJsonBytes( 'R', '#game-io', self.MOVE )
    # Send availble points to the browser
    self.__send( self.__genJsonBytes( 'R', '#move', str( move ) ) )
    # Recieve an input button pin
    pin = 0
    while pin != 07: # Button A
      self.sendReadyToRecieve()
      pin = self.__recv( 4 )
      # If up/down adjust output display accordingly
      if pin == 65: # Up
        if move < self.points:
          move += 1
          self.__send( self.__genJsonBytes( 'R', '#move', str( move ) ) )
      elif pin == 66: # Down
        if move > 0:
          move -= 1
          self.__send( self.__genJsonBytes( 'R', '#move', str( move ) ) )
    self.__send( self.__genJsonBytes( 'R', '#move', '' ) )
    return move

  # Construct the json to be sent by the wssocket server
  def __genJsonBytes( self, cmd, target, content ):
    content = content.replace( '"', '\\"' ).replace( '\n' , ' ' )
    return bytes( '{"cmd":"' + cmd + '","target":"' + target + '","content":"' + content + '"}', 'utf-8' )

  # Send data to the game launcher to be passed on to the wssocket server
  def __send( self, data ):
    if self.__sock is not None:
      size = struct.pack( '>I', len( data ) )
      self.__sock.send( size + data )

  def __sendReadyToRecieve( self ):
    self.__sock.send( b'\xab\xba\xfa\xce' )
  
  # Recieve a selected pin number
  def __recv( self ):
    if self.__sock is not None:
      pin = self.__sock.recv( 4 )
      return int( struct.unpack( '>I', pin )[ 0 ] )
# ------------------------------------
