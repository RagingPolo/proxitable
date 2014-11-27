# Start the WebSocketServer: python3 wsserver.py
# Load the file 'client.html' in a browser and click connect
#  The connect button should disappear is the connection was successful
# Run this script passing any html as argv1 and it should appear on the web page

import socket
import struct
import sys

sock = socket.socket()
sock.connect( ( '127.0.0.1', 9000 ) )
data = bytes( sys.argv[ 1 ], 'utf-8' )
size = struct.pack( '>I', len( data ) )
sock.send( size + data )
