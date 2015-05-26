/******************************************************************************
 * Run game and enforce game logic                                           */
function BtlGame( bsize, view ) {
  this.size = bsize;
  this.view = view;
  this.players = { 'human' : new BtlPlayer( 'Player 1', bsize ),
                   'bot' : new BtlPlayer( 'Player 2', bsize ) };
  this.bot = new BtlBot( bsize );
  this.selected = [ 0, 0 ];
  this.winner = 0;
  this.view.placeHumanShips( this.players[ 'human' ].getBoard().getShips() );
  this.view.setAim( this.selected );
}
BtlGame.prototype.run = function() {
  var self = this;
  // Turn the correct PES buttons on
  var pinStat = { "UP": true, "DOWN": true, "LEFT": true, "RIGHT": true,
                  "SELECT": false, "START": false, "A": true, "B": false };
  $.ajax( {
    type: "POST",
    url: "http://10.0.0.1:8080/pins",
    contentType: "application/json",
    dataType: "json",
    data: pinStat,
  }).done( function() {
    console.log( 'PES button setup complete' );
  }).fail( function() {
    console.log( 'PES button setup failed' );
  });
  // Allows for keyboard to simulate pes input
  $( 'html' ).keydown( function ( e ) {
    var keyMap = { 37 : 'LEFT', 39 : 'RIGHT', 38 : 'UP', 40 : 'DOWN',
                   13 : 'START', 83 : 'SELECT', 65 : 'A', 66 : 'B' };
    if ( e.which in keyMap ) {
      self.handleInput( keyMap[ e.which ] );
    }
  });
  this.ajax();
};
BtlGame.prototype.ajax = function() {
  var self = this;
  $.ajax( {
    type: "GET",
    url: "http://10.0.0.1:8080/pressed",
    dataType: "json",
  }).done( function( data, textStatus, jqXHR  ) {
    self.handleInput( data.button );
    // After the request has returned call again
    self.ajax();
  }).fail( function( jqXHR, textStatus, errorThrown ) {
    console.log( 'Button request failed: ' + textStatus );
    // After the request has returned call again
    self.ajax();
  });  
};
// Handle the user input forom pes/keyboard
BtlGame.prototype.handleInput = function( button ) {
  switch ( button ) {
    case 'LEFT':
      if ( this.selected[ 0 ] > 0 ) {
        --this.selected[ 0 ];
      }
      this.view.setAim( this.selected );
      break;
    case 'RIGHT':
      if ( this.selected[ 0 ] < ( this.size - 1 ) ) {
        ++this.selected[ 0 ];
      }
      this.view.setAim( this.selected );
      break;
    case 'UP':
      if ( this.selected[ 1 ] > 0 ) {
        --this.selected[ 1 ];
      }
      this.view.setAim( this.selected );
      break;
    case 'DOWN':
      if ( this.selected[ 1 ] < ( this.size - 1 ) ) {
        ++this.selected[ 1 ];
      }
      this.view.setAim( this.selected );
      break;
    case 'A':
      // Play the human players move
      var move, bmove;
      if ( 0 == this.winner ) {
        this.view.showMsg( '' );
        move = new BtlMove( this.selected[ 0 ], this.selected[ 1 ] );
        if ( this.players.human.alreadyPlayed( move ) ) {
          this.view.showMsg( "You have already played that move." );
          break;
        }
        move.setHit( this.players.bot.getBoard().takeShot( move ) );
        this.players.human.addMove( move );
        if ( move.isHit() ) {
          this.view.addHit( 'bot', move );
          this.view.setAim( this.selected );
        } else {
          this.view.addMiss( 'bot', move );
          this.view.setAim( this.selected );
        }
        this.checkWinner();  
      }
      // Play bot move
      if ( 0 == this.winner ) {
        bmove = this.bot.getMove( this.players.bot.getHistory() );
        move = new BtlMove( bmove[ 0 ], bmove[ 1 ] );
        move.setHit( this.players.human.getBoard().takeShot( move ) );
        this.players.bot.addMove( move );
        if ( move.isHit() ) {
          this.view.addHit( 'hum', move );
          this.view.setAim( this.selected );
        } else {
          this.view.addMiss( 'hum', move );
          this.view.setAim( this.selected );
        }
        this.checkWinner();  
      }
      break;
    default:
      break;
  }
};
// Check if we have a winner return player number or zero if no winner
BtlGame.prototype.checkWinner = function() {
  if ( this.players.bot.getBoard().isAllSunk() ) {
    this.winner = 1;
    this.view.showMsg( "Well done, you win!" );
  }
  if ( this.players.human.getBoard().isAllSunk() ) {
    this.winner = 2;
    this.view.showMsg( "Your fleet is sunk, you lose!" );
  }
};
