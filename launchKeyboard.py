#!/opt/python3.4/bin/python3.4
import os
import sys
import struct
import socket
import select
import logging
from time import sleep
import imp
import importlib
from GlOutAbstract import GlOutAbstract
from GlInAbstract import GlInAbstract
from GlOutWss import GlOutWss
from GlInKeyboard import GlInKeyboard
import RPi.GPIO as GPIO
import atexit
# --------------------------------------------------------------------------- #
# CLASS Launcher
#
# Load input and output modules. Load available games, launch games on request. 
# Run games in forked child handling IO with game and the output and input 
# modules.
# --------------------------------------------------------------------------- #
class Launch( object ):

  PIN_IN  = [ 26, 23, 21, 18, 15, 12, 10, 7 ]
  PIN_OUT = [ 24, 22, 19, 16, 13, 11, 8, 5 ]

  # Sets up the system wide logging, initialises the GPIO pins needed for the 
  # PES input. Searches for and load availible games
  def __init__( self ):
    # Start the logger
    LOGFORMAT = ( '[ %(levelname)s ] [ %(asctime)-15s ] [ %(process)d ] [ '
                  '%(module)s.%(funcName)s() ] [ %(message)s ]' )
    logging.basicConfig( filename='.proxitable.log', level=logging.DEBUG,
                         format=LOGFORMAT )
    logging.info( 'Started Launcher' ) 
    # Setup the launcher
    self.imod    = None
    self.omod    = None
    self.games   = self.__loadGames()
    self.__setupGPIO()
    atexit.register( self.cleanup )

  # Sets up the required GPIO pins
  def __setupGPIO( self ):
    GPIO.setmode( GPIO.BOARD )
    for pin in self.PIN_IN:
      GPIO.setup( pin, GPIO.IN )
    for pin in self.PIN_OUT:
      GPIO.setup( pin, GPIO.OUT )

  # XXX Pre games menu code. Will launch the next availble game continuosly
  def loopGames( self ):
    while True:
      for x in self.games:
        self.__runGame( x )
        sleep( 5 )

  # Called by __init__() to look for games in sub folders of current working
  # directory. Dynamically loads games and imports the correct modules based
  # on the provided config file.
  # @returns - list of game objects
  def __loadGames( self ):
    games = []
    for d in os.walk( '.' ).__next__()[ 1 ]:
      # The files main.py and main.conf are required for dynamic game loading
      if ( os.path.isfile( d + '/main.py' ) and
           os.path.isfile( d + '/main.conf' ) ):
        try:
          # Add game folder to the python path and load the main module
          sys.path.append( os.path.abspath( d ) )
          mod = imp.load_source( 'Main', d +'/main.py' )
          game = mod.Main()
          # Set up input and output from config file
          with open( d + '/main.conf' ) as ioConf:
            # main.conf file specifys the io modules to be loaded for the game
            # the file should consist of three lines
            # Line 1: Player one input module
            # Line 2: Player two input module
            # Line 3: Game output module 
            # Line format - <module name>:[args,...]
            game.setInput( 1, self.__setupIOModule( ioConf.readline() ) )
            game.setInput( 2, self.__setupIOModule( ioConf.readline() ) )
            game.setOutput( self.__setupIOModule( ioConf.readline() ) )
          games.append( game )
        except Exception as e:
          logging.exception( 'Failed loading %s', d ) 
    logging.info( '%d games loaded', len( games ) )
    return games

  # Sets up a unix domain socket for comms with the givern game. Forks and
  # calls the games .run() method in the child. Parent will recieve game output
  # and pass it on the launchers output module until the game says it is ready
  # to recieve some input. Launcher will check for input and pass it on before
  # returning to listening for output.
  #  @game - game object to be run
  def __runGame( self, game ):
    if self.omod is not None:
      try:
        os.unlink( game.getName() + '_socket' )
      except OSError:
        if os.path.exists( game.getName() + '_socket' ):
          raise
      try:
        sock = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
        sock.bind( game.getName() + '_socket' )
      except socket.error as e:
        logging.exception( 'Failed to create unix socket for %s', 
                                                              game.getName() )
        return
      if os.fork() > 0:
        # Parent - game launcher
        try:
          sock.listen( 1 )
          con, client = sock.accept()
        except socket.error as e:
          logging.exception( 'Failed to recieve connection from %s',
                                                              game.getName() )
        try:
          # Get the PES pins that need turning on
          self.__setPesPins( con, game.getName() )
          # Start Game IO
          size = con.recv( 4 )
          while len( size ) > 0:
            size_int = struct.unpack( '>I', size )[ 0 ]
            data = con.recv( size_int )
            logging.debug( '[' + str( size_int ) + '] ' + str( data ) )
            if data == b'\xab\xba\xfa\xce':
              logging.debug( 'Lets recieve stuff...' )
              # Game has said it is ready to recieve
              # so get a button pin reading and pass it on
              pin = self.imod.getButton()
              logging.debug( 'rtr pin = %d', int( pin ) )
              con.send( struct.pack( '>I', pin ) )
            else: 
              self.omod.send( size + data )
            size = con.recv( 4 )
        except socket.error as e:
          logging.exception( 'Connection to %s failed', game.getName() )
      else:
        # Child - the game
        # Try to setup the connection back to the parent and then game the run()
        # method. call exit() when finished to avoid multiple copies of the game
        # launcher running.
        try:
          game.connect( game.getName() + '_socket' )
        except socket.error as e:
          logging.exception( '%s failed to connect to launcher',
                                                             game.getName() )
          sys.exit( 1 )
        game.run()
        sys.exit( 1 )
    else:
      logging.error( 'No ouput module loaded' )

  # __runGame() helper method. Asks the game which pins are required for input
  # and turns them on. Makes sure that all others are off
  def __setPesPins( self, con, name ):
    try:
      size = con.recv( 4 )
      if len( size ) > 0:
        size_int = struct.unpack( '>I', size )[ 0 ]
        pinsBytes = con.recv( size_int )
        # Make the struct fmt
        length = int( len( pinsBytes ) / 4 )
        fmt = []
        fmt.append( '>' )
        for i in range( length ):
          fmt.append( 'I' )
        # trim pinBytes and convert to tuple
        pins = struct.unpack( ''.join( fmt ), pinsBytes[ : length * 4 ] )
        # set all pins in tuple to high
        for pin in self.PIN_OUT:
          if pin in pins:
            GPIO.output( pin, True )
          else:
            GPIO.output( pin, False )
      else:
        logging.warning( 'Failed to recieve game pins list' )
    except socket.error as e:
      logging.exception( '%s connection failed', name )

  # Using the information found in main.conf dynamicallyload the specified IO
  # module. Extract the args from the serialised list in format of [arg,arg,...]
  #  @line    - Line from main.conf containing module name and args list
  #  @returns - The loaded module or None on failure
  def __setupIOModule( self, line ):
    io = line.rstrip().split( ':' )
    if len( io ) > 1:
      ioClass = self.__importClass( io[ 0 ] )
      if len( io[ 1 ][ 1 : -1 ] ) > 0:
        args = io[ 1 ][ 1 : -1 ].split( ',' )
      else:
        args = []
      return ioClass( args )
    return None

  # Return a callable object from the imported module
  # __setupIOModule() helper method. Gets a callable object of givern module
  #  @name    - name of module to load
  #  @returns - callable object 
  def __importClass( self, name ):
    mod = importlib.import_module( name )
    return getattr( mod, name )

  # TODO Phase 2 method
  # Generate the required CSS/HTML to produce a tiled menu featuring all loaded
  # games. Output the menu and handle input launching selected game when
  # selected.
  # XXX Could implement konami code easter egg on the main menu ^^vv<><>BA 
  def genMenu( self ):
    pass
  
  # Validate against the Abstract input class and set as the game launchers
  # input module
  def setInputMod( self, imod ):
    if isinstance( imod, GlInAbstract ):
      self.imod = imod
      logging.info( 'Input module set to: %s', imod.getName() )
    else:
      logging.warning( 'Invalid input module' )

  # Validate against the Abstract output class and set as the game launchers
  # output module
  def setOutputMod( self, omod ):
    if isinstance( omod, GlOutAbstract ):
      self.omod = omod
      logging.info( 'Output module set to: %s', omod.getName() )
    else:
      logging.warning( 'Invalid output module' ) 

  # Call the IO module cleanup modules. Should be set to be called on exit 
  def cleanup( self ):
    GPIO.cleanup()
    if self.imod is not None:
      self.imod.cleanup()
    if self.omod is not None:
      self.omod.cleanup()
# ------------------------------------

if __name__ == '__main__':
  launch = Launch()
  launch.setOutputMod( GlOutWss( '', 9000 ) )
  launch.setInputMod( GlInKeyboard() )
  launch.loopGames()
