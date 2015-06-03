/******************************************************************************
 * Control the game logic and link interface with view                       */
function ConGame( view ) {
  this.view = view;
  this.board = new ConBoard();
  this.selected = 0;
  this.player = 1;
  this.winner = 0;
  this.ready = false;
  this.help = true;
}
// Run the game
ConGame.prototype.run = function() {
  var self = this;
  this.view.showMsg( 'The aim of the game is to get 4 pieces of your colour in a row. This can be horizontally, vertically or diagonally.<br /><ul><li>Press B when you are ready to play your move</li><li>Use LEFT and RIGHT to choose your column</li><li>Press A to drop a piece</li></ul><p><center>Press START to continue</center></p>', 1200, 700 );
  // Turn the correct PES buttons on
  var pinStat = { "UP": false, "DOWN": false, "LEFT": true, "RIGHT": true,
                  "SELECT": false, "START": true, "A": true, "B": true };
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
// Make api call for button press
ConGame.prototype.ajax = function() {
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
// Make game actions based on recieved input
ConGame.prototype.handleInput = function( button ) {
  var self = this;
  if ( this.help ) {
    if ( 'START' == button ) {
      this.view.showMsg( 'Player ' + this.player + ' ready?' );
      this.help = false;
      this.view.setSelected( this.selected );
    }
  } else {
    if ( 0 == this.winner ) {
      switch ( button ) {
        case 'LEFT':
          if ( ( true == this.ready ) && ( this.selected > 0 ) ) {
            --this.selected;
            this.view.setSelected( this.selected );
          }
          break;
        case 'RIGHT':
          if ( ( true == this.ready ) && ( this.selected < this.board.getWidth() - 1 ) ) {
            ++this.selected;
            this.view.setSelected( this.selected );
          } 
          break;
        case 'A':
          if ( true == this.ready ) {
            var id;
            var msg = '';
            if ( ( id = this.board.drop( this.selected, this.player ) ) ) {
              this.view.drop( id, this.player );
              this.player = ( 1 == this.player ) ? 2 : 1;
              if ( ( this.winner = this.board.winner() ) ) {
                msg = 'Player ' + this.winner + ' Wins!';
              } else {
                if ( this.board.full() ) {
                  msg = 'It\'s a draw...'; 
                }
              }
              if ( msg ) {
                this.view.showMsg( msg );
                setTimeout( function() {
                  self.view.fadeMsg( 2000 );
                }, 3000 );
                this.view.hideSelected();
                // Return to main menu
                setTimeout( function() { 
                  var url = window.location.href;
                  url = url.substring( 0, url.lastIndexOf( "/" ) + 1 ) + "../index.html";
                  window.location.replace( url );
                }, 7000 );
              } else {
                // We have another go
                this.ready = false;
                this.view.showMsg( 'Player ' + this.player + ' ready?' );
              }
            }
          }
          break;
        case 'B':
          if ( false == this.ready ) {
            this.ready = true;
            this.view.fadeMsg( 500 );
          }
          break;
        default:
          break;
       } 
    }
  }
}
