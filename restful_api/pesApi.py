from flask import Flask, jsonify, request
import RPi.GPIO as GPIO
from time import sleep
from flask.ext.cors import cross_origin

app = Flask( __name__ )
# Relevent pins for the PES hardware
INPUT_PINS  = { 'UP' : 23,
                'DOWN' : 18,
                'LEFT' : 26,
                'RIGHT' : 21,
                'START' : 12,
                'SELECT' : 15,
                'A' : 7, 
                'B' : 10 }
OUTPUT_PINS = { 'UP' : 22,
                'DOWN' : 16,
                'LEFT' : 24,
                'RIGHT' : 19,
                'START' : 11,
                'SELECT' : 13,
                'A' : 5,
                'B' : 8 }

@app.route( '/pins', methods = [ 'GET', 'POST' ] )
@cross_origin( allow_headers=['Content-Type'] )
def pins():
  status = {}
  if request.method == 'POST':
    if request.headers[ 'Content-Type' ] == 'application/json':
      for button in request.data.decode( 'utf-8' ).split( '&' ):
        kv = button.split( '=' )      
        status[ kv[ 0 ] ] = True if kv[ 1 ] == 'true' else False
      for button, setting in status.items():
        if button in OUTPUT_PINS:
          GPIO.output( OUTPUT_PINS[ button ], setting )
    return "", 204, {}
  if request.method == 'GET':
    for button in OUTPUT_PINS:
      status[ button ] = True if GPIO.output( OUTPUT_PINS[ button ] ) == 1 else False
    return jsonify( status )

@app.route( '/pressed', methods = [ 'GET' ] )
def pressed():
  # Poll GPIO pins
  pressed = None
  while True:
    for button in INPUT_PINS:
      if GPIO.input( INPUT_PINS[ button ] ):
        pressed = button
        break
    sleep( 0.1 )
  return jsonify( { 'button' : pressed } )

if '__main__' == __name__:
  # Setup the GPIO pins
  GPIO.setmode( GPIO.BOARD )
  for button, pin in INPUT_PINS.items():
    GPIO.setup( pin, GPIO.IN )
  for button, pin in OUTPUT_PINS.items():
    GPIO.setup( pin, GPIO.OUT )
  app.run( host='0.0.0.0', port=8080, threaded=True )
