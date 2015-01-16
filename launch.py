#!/usr/bin/env python3
import os
import sys
import struct
import socket
import select
import logging
from time import sleep
import importlib.machinery
from GlOutAbstract import GlOutAbstract
from GlInAbstract import GlInAbstract
from GlOutWss import GlOutWss
from GlInProxitable import GlInProxitable
# import RPi.GPIO as GPIO
# ------------------------------------
# CLASS Launcher
#
# Load input and output modules. Load
# available games, launch selected 
# game and support its IO when 
# requested. Regain execution when 
# game finishes
# ------------------------------------
class Launch( object ):

  def __init__( self, timeout=10 ):
    # Start the logger
    LOGFORMAT = '[ %(levelname)s ] [ %(asctime)-15s ] [ %(process)d ] [ %(module)s.%(funcName)s() ] [ %(message)s ]'
    logging.basicConfig( filename='.proxitable.log', level=logging.DEBUG, format=LOGFORMAT )
    logging.info( 'Started Launcher' ) 
    # Setup the launcher
    self.imod    = None
    self.omod    = None
    self.timeout = timeout
    self.games = self.__loadGames()
    #self.__setupGPIO()

#  def __setupGPIO.IN self ):
#    GPIO.setmode( GPIO.BOARD )
#    GPIO.setup( 5, GPIO.OUT )
#    GPIO.setup( 7, GPIO.IN )
#    GPIO.setup( 8, GPIO.OUT )
#    GPIO.setup( 10, GPIO.IN )
#    GPIO.setup( 11, GPIO.OUT )
#    GPIO.setup( 12, GPIO.IN )
#    GPIO.setup( 13, GPIO.OUT )
#    GPIO.setup( 15, GPIO.IN )
#    GPIO.setup( 16, GPIO.OUT )
#    GPIO.setup( 18, GPIO.IN )
#    GPIO.setup( 19, GPIO.OUT )
#    GPIO.setup( 21, GPIO.IN )
#    GPIO.setup( 22, GPIO.OUT )
#    GPIO.setup( 23, GPIO.IN )
#    GPIO.setup( 24, GPIO.OUT )
#    GPIO.setup( 26, GPIO.IN )
    
  # Test code
  def test( self ):
    while True:
      for x in self.games:
        self.__runGame( x )
        sleep( 5 )

  def __loadGames( self ):
    games = []
    for d in os.walk( '.' ).__next__()[ 1 ]:
      if ( os.path.isfile( d + '/main.py' ) and
           os.path.isfile( d + '/main.conf' ) ):
        try:
          # Add game folder to the python path and load the main module
          sys.path.append( os.path.abspath( d ) )
          mod = importlib.machinery.SourceFileLoader( 'Main', d + '/main.py' ).load_module()
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
        logging.exception( 'Failed to create unix socket for %s', game.getName() )
        return
      if os.fork() > 0:
        # Parent - game launcher
        try:
          sock.listen( 1 )
          con, client = sock.accept()
        except socket.error as e:
          logging.exception( 'Failed to recieve connection from %s', game.getName() )
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
        try:
          game.connect( game.getName() + '_socket' )
        except socket.error as e:
          logging.exception( '%s failed to connect to launcher', game.getName() )
          sys.exit( 1 )
        game.run()
        sys.exit( 1 )
    else:
      logging.error( 'No ouput module loaded' )

  # Get which pins need turing on from the game
  # and set them to high
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
        for pin in pins:
          pass
          # GPIO.output( pin, True )
      else:
        logging.warning( 'Failed to recieve game pins list' )
    except socket.error as e:
      logging.exception( '%s connection failed', name )

  # Load specified io module and instantiate with givern args
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
  def __importClass( self, name ):
    mod = importlib.import_module( name )
    return getattr( mod, name )

  # Using information from the games object generate
  # the load menu to be displayed to the user
  def genMenu( self ):
    pass

  def setInputMod( self, imod ):
    if isinstance( imod, GlInAbstract ):
      self.imod = imod
      logging.info( 'Input module set to: %s', imod.getName() )
    else:
      logging.warning( 'Invalid input module' )

  def setOutputMod( self, omod ):
    if isinstance( omod, GlOutAbstract ):
      self.omod = omod
      logging.info( 'Output module set to: %s', omod.getName() )
    else:
      logging.warning( 'Invalid output module' ) 
 
  def cleanup( self ):
    if self.imod is not None:
      self.imod.cleanup()
    if self.omod is not None:
      self.omod.cleanup()
# ------------------------------------

if __name__ == '__main__':
  launch = Launch()
  launch.setOutputMod( GlOutWss( '', 9000 ) )
  launch.setInputMod( GlInProxitable() )
  launch.test()
  launch.cleanup()
