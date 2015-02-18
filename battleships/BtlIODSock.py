from GlBasicGameIO import GlBasicGameIO
from BtlOutAbstract import BtlOutAbstract
from BtlInAbstract import BtlInAbstract
import logging
import socket
import struct

# ---------------------------------------------------------------------------- #
# CLASS BtlIODSock
#
# Combines the input and output modules for the citadel game. This allows them
# to share a socket for two way comms with the game launcher
# ---------------------------------------------------------------------------- #
class BtlIODSock( BtlInAbstract, BtlOutAbstract, GlBasicGameIO ):

  CSS = ( '.square{float:left;margin:1px;position:relative;width:3.8%;'
          'padding-bottom:3.8%;overflow:hidden;}'
          '.content{position:absolute;height:100%;width:100%;}'
          '.centre{position:absolute;top:50%;left:50%;transform:'
          'translateX(-50%)translateY(-50%);font-family:"devroyeregular",'
          'serif;}'
          '.water{background-color:#0066CC;}'
          '.ship{background-color:#444444;}'
          '.axis{background-color:#AAAAAA;}'
          '.image{max-width:100%;max-height:100%;}'
          '@font-face{font-family:"devroyeregular";'
          'src:url("resources/font/battleships/DEVROYE_-webfont.eot");'
          'src:url("resources/font/battleships/DEVROYE_-webfont.eot?#iefix")'
          'format("embedded-opentype"),'
          'url("resources/font/battleships/DEVROYE_-webfont.woff")'
          'format("woff"),'
          'url("resources/font/battleships/DEVROYE_-webfont.ttf")'
          'format("truetype"),'
          'url("resources/font/battleships/DEVROYE_-webfont.svg#devroyeregular")'
          'format("svg");font-weight:normal;font-style:normal;}' )
  CELL = ( '<div id="" class="square">'
           '  <div class="content">'
           '    <div class="centre">'
           '    </div>'
           '  </div>'
           '</div>' )
  HIT = '<img class="image" src="resources/images/battleships/hit.png" />'
  MISS = '<img class="image" src="resources/images/battleships/miss.png" />'
