from flask import Flask, jsonify, request
import RPi.GPIO as GPIO
from time import sleep

# TODO create a dict to map button names, UP, DOWN, etc to pin numbers
#      so that the pins are abstracted for the client side code

app = Flask( __name__ )
# Relevent pins for the PES hardware
INPUT_PINS  = [ 12, 23, 18, 21, 26, 7, 10, 15 ]
OUTPUT_PINS = [ 24, 22, 19, 16, 13, 11, 8, 5 ]

@app.route( '/pins', methods = [ 'GET', 'PUT', 'OPTIONS' ] )
def pins():
  # Send a response that will allow cross domain requests
  if request.method == 'OPTIONS':
    return "", 200, {
      'Access-Control-Allow-Origins' : '*',
      'Access-Control-Allow-Methods' : 'PUT,GET',
      'Access-Control-Allow-Headers' : 'Content-Type'
    }
  if request.method == 'GET':
    # Poll all pins output pins and return status
    status = {}
    for pin in OUTPUT_PINS:
      status[ pin ] = True if GPIO.output( pin ) else False
    return jsonify( status )
  if request.method == 'PUT': 
    if request.headers[ 'Content-Type' ] == 'application/json':
      status = request.json
      # Update all off the output pins
      for pin, setting in status:
        if pin in OUTPUT_PINS:
          # TODO Should have some exception handling in case setting isn't boolean
          GPIO.output( pin, setting )
          # TODO Also how do we want the hardware to behave if the user trys to set
          #      an invalid pin, ignore? bail? undo all changes?
      # Success - No Content
      return "", 204, {}
    # Not json - Unsupported Media Type
    return "", 415, {}
  # Bad request - Method Not Allowed
  return "", 405, {}

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
  for pin in INPUT_PINS:
    GPIO.setup( pin, GPIO.IN ):
  for pin in OUTPUT_PINS:
    GPIO.setup( pin, GPIO.OUT ):
  app.run( host='0.0.0.0', port=8080, threaded=True )
