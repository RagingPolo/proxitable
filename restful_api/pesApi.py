from flask import Flask, jsonify, request
import RPi.GPIO as GPIO
from time import sleep
from flask.ext.cors import cross_origin

app = Flask( __name__ )
# Relevent pins for the PES hardware
INPUT_PINS  = { 'UP' : 13,
                'DOWN' : 31,
                'LEFT' : 11,
                'RIGHT' : 15,
                'START' : 33,
                'SELECT' : 29,
                'A' : 37, 
                'B' : 35 }
OUTPUT_PINS = { 'UP' : 16,
                'DOWN' : 32,
                'LEFT' : 12,
                'RIGHT' : 18,
                'START' : 36,
                'SELECT' : 22,
                'A' : 40,
                'B' : 38 }

@app.route( '/pins', methods = [ 'POST' ] )
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

@app.route( '/pressed', methods = [ 'GET' ] )
@cross_origin( allow_headers=['Content-Type'] )
def pressed():
  # Poll GPIO pins
  pressed = None
  while pressed == None:
    for button, pin in INPUT_PINS.items():
      if GPIO.input( pin ):
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
