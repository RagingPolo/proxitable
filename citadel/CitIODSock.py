from CitOutAbstract import CitOutAbstract
from CitInAbstract import CitInAbstract
import socket
import struct
import json
import logging

# TODO Some of these methods will apply to any game using the
# proxitable and game launcher -> make a parent class

# ---------------------------------------------------------------------------- #
# CLASS CitIOSock
#
# Combines the input and output modules for the citadel game. This allows them
# to share a socket for two way comms with the game launcher
# ---------------------------------------------------------------------------- #
class CitIODSock( CitInAbstract, CitOutAbstract ):

  CSS = ( '.display { background-color: #0000AF; color: #FFF; vertical-align:'
          ' middle; float: left; -webkit-border-radius: 1%; -moz-border-radius:'
          ' 1%; border-radius: 10px; }'
          '.player-display { margin: 1% 10% 1% 10%; height: 80%; width: 30%; }'
          '.position-display { margin: 1% 1% 1% 1%; height: 50px; width: 12%; }'
          '.container { width: 80%; margin: 0.5% auto; overflow: hidden; }'
          '.player-container { height: 30%; }' )
  HTML = ( '<div class="container player-container">'
           '  <div id="player_one" class="display player-display">'
           '    <h1 id="p2_name">Player One</h1>'
           '    <h2 id="p1_points">50</h2>'
           '  </div>'
           '  <div id="player_two" class="display player-display">'
           '    <h1 id="p2_name">Player Two</h1>'
           '    <h2 id="p2_points">50</h2>'
           '  </div>'
           '</div>'
           '<br />'
           '<div class="container">'
           '  <div id="pos0" class="display position-display"></div>'
           '  <div id="pos1" class="display position-display"></div>'
           '  <div id="pos2" class="display position-display"></div>'
           '  <div id="pos3" class="display position-display"></div>'
           '  <div id="pos4" class="display position-display"></div>'
           '  <div id="pos5" class="display position-display"></div>'
           '  <div id="pos6" class="display position-display"></div>'
           '</div>' )
  MOVE = '<center><h1 id="move"></h1></center>'

  # Pins to turn on the required buttons for input
  PIN_TURN_ON = [ 5, 16, 22 ]

  # Overiding __new__ to enforce a singleton design pattern
  __instance = None
  def __new__( cls, val ):
    if CitIODSock.__instance is None:
      CitIODSock.__instance = object.__new__( cls )
    CitIODSock.__instance.val = val
    return CitIODSock.__instance

  # Setup the module by calling both super inits
  #  @args - empty list (this allows for the use of the generic module loader)
  def __init__( self, args ):
    CitInAbstract.__init__( self, False )
    CitOutAbstract.__init__( self )
    self.__sock   = None
    self.ai       = False
    self.__points = 50
    self.__last   = 1

  # Used to set up link to game launcher
  #  @addr - address of the unix domain socket
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

  # Return a serialised list of pin numbers to turn on for the game
  def getTurnOnPins( self ):
    pins = []
    for pin in self.PIN_TURN_ON:
      pins.append( struct.pack( '>I', pin ) )
    return b''.join( pins )  

  # Display the game in it's starting state
  def newGame( self ):
    # Tell the launcher which pins need to be set to high
    self.__send( self.getTurnOnPins() )
    # Clear anything that may or may not be on the browser
    self.__send( self.__genJsonBytes( 'R', '#game-css', '' ) )
    self.__send( self.__genJsonBytes( 'R', '#game-html', '' ) )
    self.__send( self.__genJsonBytes( 'R', '#game-io', '' ) )
    # Now send the game starting state
    self.__send( self.__genJsonBytes( 'R', '#game-css', self.CSS ) )
    self.__send( self.__genJsonBytes( 'R', '#game-html', self.HTML ) )

  # Display the current game state
  #  @pos - board position : 0-6 
  #  @p1p - player one points : 0-50
  #  @p2p - player two points : 0-50
  #  @p1m - player one last move : int
  #  @p2m - player two last move : int
  def showState( self, pos, p1p, p2p, p1m, p2m ):
    self.__send( self.__genJsonBytes( 'R', '#p1_points', str( p1p ) ) )    
    self.__send( self.__genJsonBytes( 'R', '#p2_points', str( p2p ) ) )
    self.__send( self.__genJsonBytes( 'X', 'None', '$( ".position-display" )'
                                    '.css( "background-color", "#0000AF" );' ) )
    self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos' + str( pos ) +
                                    '" ).css( "background-color", "#000" );' ) )

  # Display the game result
  #  @result - the game result : P1, P2, DRAW
  def showResult( self, result ):
    winner = ''
    if result == self.P1:
      winner = 'Player One Wins'
    elif result == self.P2:
      winner = 'Player Two Wins'
    elif result == self.DRAW:
      winner = 'Draw!'
    self.__send( self.__genJsonBytes( 'R', '#game-io', '<center><b>Game Over: '
                                                  + winner + '</b></center>' ) )

  # Get a players move from the proxitable hardware through the game launcher 
  #  @name    - name of player entering move
  #  @points  - players current points total
  #  @last    - opponents last move ( to aid AI players )
  #  @returns - move ( positive integer no greater than points )
  def getMove( self, name, points, last ):
    move = self.__last if self.__last <= self.__points else self.__points
    self.__send( self.__genJsonBytes( 'R', '#game-io', self.MOVE ) )
    # Send availble points to the browser
    self.__send( self.__genJsonBytes( 'R', '#move', str( move ) ) )
    # Recieve an input button pin
    pin = 0
    while pin != 7: # Button A
      self.__sendReadyToRecieve()
      pin = self.__recv()
      # If up/down adjust output display accordingly
      if pin == 23: # Up
        if move < self.__points:
          move += 1
          self.__send( self.__genJsonBytes( 'R', '#move', str( move ) ) )
      elif pin == 18: # Down
        if move > 1:
          move -= 1
          self.__send( self.__genJsonBytes( 'R', '#move', str( move ) ) )
    self.__send( self.__genJsonBytes( 'R', '#move', '' ) )
    # Record values ready for next turn before returning move to game
    self.__points -= move
    self.__last = move
    return move

  # Construct the json to be sent by the wssocket server
  #  @cmd     - Single char command as described in client.html
  #  @target  - id or class of target DOM element
  #  @content - data to be used by command on target
  #  @returns - fully constructed JSON object
  def __genJsonBytes( self, cmd, target, content ):
    content = content.replace( '"', '\\"' ).replace( '\n' , ' ' )
    return bytes( '{"cmd":"' + cmd + '","target":"' + target + '","content":"'
                                                     + content + '"}', 'utf-8' )

  # Send data to the game launcher to be passed on to the wssocket server
  #  @data - data to be sent as bytes object
  def __send( self, data ):
    if self.__sock is not None:
      size = struct.pack( '>I', len( data ) )
      self.__sock.send( size + data )
  
  # Send the flag to say that the module is ready to recieve a pin value
  def __sendReadyToRecieve( self ):
    logging.debug( '' )
    self.__send( b'\xab\xba\xfa\xce' )
  
  # Recieve a selected pin number
  def __recv( self ):
    if self.__sock is not None:
      pin = self.__sock.recv( 4 )
      if len( pin ) != 4:
        logging.debug( 'pin len = ' + str( len( pin ) ) )
        return 0
      return int( struct.unpack( '>I', pin )[ 0 ] )
# ---------------------------------------------------------------------------- #
