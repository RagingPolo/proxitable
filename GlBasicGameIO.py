import logging
import struct

# ---------------------------------------------------------------------------- #
# CLASS BasicGameIO
#
# Provided the basic methods required by all games to enable input/output comms
# with the game launcher.
# ---------------------------------------------------------------------------- #
class BasicGameIO( object ):
  
  # Construct the json to be sent by the wssocket server
  #  @cmd     - Single char command as described in client.html
  #  @target  - id or class of target DOM element
  #  @content - data to be used by command on target
  #  @returns - fully constructed JSON object
  def genCmd( self, cmd, target, content ):
    content = content.replace( '"', '\\"' ).replace( '\n' , ' ' )
    return bytes( '{"cmd":"' + cmd + '","target":"' + target + '","content":"'
                                                     + content + '"}', 'utf-8' )
  # Send data to the game launcher to be passed on to the wssocket server
  #  @data - data to be sent as bytes object
  def send( self, data ):
    if self.__sock is not None:
      size = struct.pack( '>I', len( data ) )
      self.__sock.send( size + data )
  
  # Send the flag to say that the module is ready to recieve a pin value
  def sendReadyToRecieve( self ):
    logging.debug( '' )
    self.send( b'\xab\xba\xfa\xce' )
  
  # Recieve a selected pin number
  def recv( self ):
    if self.__sock is not None:
      pin = self.__sock.recv( 4 )
      if len( pin ) != 4:
        logging.debug( 'pin len = ' + str( len( pin ) ) )
        return 0
      return int( struct.unpack( '>I', pin )[ 0 ] )
# ---------------------------------------------------------------------------- #
