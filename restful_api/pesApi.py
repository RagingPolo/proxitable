from flask import Flask, jsonify, request
import RPi.GPIO as GPIO
from time import sleep
from flask.ext.cors import cross_origin

app = Flask( __name__ )
# Relevent pins for the PES hardware
INPUT_PINS  = { 'START' : 12, 'UP' : 23, 'DOWN' : 18, 'RIGHT' : 21,
                'LEFT' : 26, 'A' : 7, 'B' : 10, 'SELECT' : 15 }
OUTPUT_PINS = { 'LEFT' : 24, 'UP' : 22, 'RIGHT' : 19,'DOWN' : 16,
                'SELECT' : 13, 'START' : 11, 'B' : 8, 'A' : 5 }

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
    return "", 204, {}

@app.route( '/pressed', methods = [ 'GET' ] )
def pressed():
  # Poll GPIO pins
  pin = 0
  while pin == 0:
    for i in INPUT_PINS:
      if GPIO.input( i ):
        pin = i
        break
    sleep( 0.1 )
  pressed = { 'button' : pin }
  return jsonify( pressed )

if '__main__' == __name__:
  # Setup the GPIO pins
  GPIO.setmode( GPIO.BOARD )
  for button, pin in INPUT_PINS.items():
    GPIO.setup( pin, GPIO.IN )
  for button, pin in OUTPUT_PINS.items():
    GPIO.setup( pin, GPIO.OUT )
  app.run( host='0.0.0.0', port=8080, threaded=True )
