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

  CSS = ( '.blah{}'
          '.gameView { width: 100%; position: fixed; bottom: 0;}'
          '.players { width: 100%; position: fixed; top: 0; padding-left: 15px; padding-right: 15px;}'
          '.wrapper {width: 100%;height: 100%; min-height: 100%; display: table;}'
          '.wrapper-inner { display: table-cell; vertical-align: top;}'
          '.moveNo {width: 100%; position: fixed; bottom: 0;padding-left: 40%; padding-bottom: 15px;}'
          '#game-io {width: 100%; position: fixed; top: 40%; text-align: center; font-size: 3em;}'
          '@font-face {'
          'font-family: "devroyeregular";'
            'src: url("font/DEVROYE_-webfont.eot");'
            'src: url("font/DEVROYE_-webfont.eot?#iefix") format("embedded-opentype"),'
                 'url("font/DEVROYE_-webfont.woff") format("woff"),'
                 'url("font/DEVROYE_-webfont.ttf") format("truetype"),'
                 'url("font/DEVROYE_-webfont.svg#devroyeregular") format("svg");'
            'font-weight: normal;'
            'font-style: normal; }'
            'body { height: 100%; background-color: #40c0f0!important; color: #fff ;font-family:'
            '"devroyeregular", serif;}'        )
  HTML = ( '<div class="players">'
   '<img src="images/clouds.png" style="position:absolute;top:0;" width="100%">'
      '<div id="player_one" class="pull-left">'
        '<h1 id="p2_name">Player One</h1>'
        '<h2 id="p1_points">50</h2>'
      '</div>'
      '<div id="player_two" class="pull-right">'
        '<h1 id="p2_name">Player Two</h1>'
        '<h2 id="p2_points">50</h2>'
      '</div>'
    '</div>'
 '<div class="gameView">'
   '<img src="images/bg.png" width="100%">'
   '<img id="redCastle" src="images/castleRed.png" width="11%"' 
   'style="position:absolute;bottom:80%;left:1%">'
   '<img id="blueCastle" src="images/castleBlue.png" width="11%" style="'
   'position:absolute;bottom:77%;right:1%">'
   '<img id="redTower" src="images/towerRed.png" width="5%"'
   'style="position:absolute;bottom:53%;left:25%">'
   '<img id="blueTower" src="images/towerBlue.png" width="5%" '
   'style="position:absolute;bottom:54%;right:24%">'
   '<img id="pos" src="images/position.png" width="6%" style="position:absolute;bottom:43%;right:45%">'
 '</div>' )
  MOVE = ( '<div class="moveNo">'
   '<img src="images/sword.png" width="5%" style="position:absolute;bottom:15;left:35%">'
   '<h1 id="move"></h1>'
 '</div>' )

  # Pins to turn on the required buttons for input
  PIN_TURN_ON = [ 5, 16, 22 ]
  #CSS postioning for the fighting army (only for pos1-5)
  POSITION = ['position:absolute;bottom:77%;left:4%', 'position:absolute;bottom:49%;left:24%', 'position:absolute;bottom:43%;right:45%', 'position:absolute;bottom:50%;right:23%', 'position:absolute;bottom:74%;right:4%']
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
    if pos == 0:
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos" ).hide();' ) )
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#redCastle" ).attr( "src", "images/castleBlueWin.png" );' ) )
    elif pos == 1:
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#redTower" ).attr( "src", "images/towerBlue.png" );' ) )
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos" ).attr( "style", "'+self.POSITION[pos - 1]+'" );' ) )
    elif pos == 2:
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#redTower" ).attr( "src", "images/towerRed.png" );' ) )
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos" ).attr( "style", "'+self.POSITION[pos - 1]+'" );' ) )
    elif pos == 4:
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#blueTower" ).attr( "src", "images/towerBlue.png" );' ) )
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos" ).attr( "style", "'+self.POSITION[pos - 1]+'" );' ) )
    elif pos == 5:
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#blueTower" ).attr( "src", "images/towerRed.png" );' ) )
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos" ).attr( "style", "'+self.POSITION[pos - 1]+'" );' ) )
    elif pos == 6:
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos" ).hide();' ) )
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#blueCastle" ).attr( "src", "images/castleRedWin.png" );' ) )
    else:
      self.__send( self.__genJsonBytes( 'X', 'None', '$( "#pos" ).attr( "style", "'+self.POSITION[pos - 1]+'" );' ) )

  # Display the game result
  #  @result - the game result : P1, P2, DRAW
  def showResult( self, result ):
    winner = ''
    if result == self.P1:
      winner = '<div class="gameEnd"><img src="images/win.png" width="8%"> Player One Wins</div>'
    elif result == self.P2:
      winner = '<div class="gameEnd"><img src="images/win.png" width="8%">Player Two Wins</div>'
    elif result == self.DRAW:
      winner = '<div class="gameEnd">It\'s a Draw!</div>'
    self.__send( self.__genJsonBytes( 'A', '#game-io',winner ) )

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
