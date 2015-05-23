/******************************************************************************
 * Contains game logic and maintains overall game                            */
function CitGame( state ) {
  // Turn the correct PES buttons on
  var pinStat = { "UP": true, "DOWN": true, "LEFT": false, "RIGHT": false,
                  "SELECT": false, "START": true, "A": true, "B": false };
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
  this.winner = 0;
  this.help   = 1;
  this.move   = 1;
  this.delay  = 0;
  this.board  = new CitBoard();
  this.bot    = new CitBot();
  this.player = { 1 : new CitPlayer( 'Player 1' ),
                  2 : new CitPlayer( 'Player 2' ) };
  this.state = state;
}
CitGame.prototype.ajax = function() {
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
CitGame.prototype.handleInput = function( button ) {
  if ( !this.winner ) {
    switch ( button ) {
      case 'UP':
        // Increase the propsed move by one
        if ( !( CitUpdateInstructionsVisible( this.state ) ) &&
              ( CitUpdateBoardVisible( this.state ) ) ) {
          if ( this.move < this.player[ 1 ].getPoints() ) {
            ++this.move;
            CitUpdateBid( this.state, this.move );
          }
        }
        break;
      case 'DOWN':
        // Decrease the proposed move by one
        if ( !( CitUpdateInstructionsVisible( this.state ) ) &&
              ( CitUpdateBoardVisible( this.state ) ) ) {
          if ( this.move > 1 ) {
            --this.move;
            CitUpdateBid( this.state, this.move );
          }
        }
        break;
      case 'A':
        if ( !( CitUpdateInstructionsVisible( this.state ) ) &&
              ( CitUpdateBoardVisible( this.state ) ) ) {
          CitUpdateToggleMoveBoard( this.state, this.move );
          // Play the current amount of points and get a move from the bot
          this.player[ 2 ].addMove( this.bot.getMove( this.player[ 2 ].getPoints(),
                                                      this.player[ 1 ].getLastMove() ) );
          // Add the human players move second so the bot doesn't know what the move is
          this.player[ 1 ].addMove( this.move );
          // Perform the move
          if ( this.player[ 1 ].getLastMove() > this.player[ 2 ].getLastMove() ) {
            this.board.moveRight();
          } else if ( this.player[ 1 ].getLastMove() < this.player[ 2 ].getLastMove() ) {
            this.board.moveLeft();
          }
          // Update the view
          CitUpdatePos( this.state, this.board.getPosition() );
          CitUpdatePoints( this.state, this.player[ 1 ].getPoints(), this.player[ 2 ].getPoints() );
          if ( this.move > this.player[ 1 ].getPoints() ) {
            this.move = this.player[ 1 ].getPoints();
          }
          // Set a 3 second delay that will ignore any button presses except help (START)
          this.delay = 1;
          var self = this;
          setTimeout( function() { 
            self.delay = 0;
            if ( !self.winner ) {
              CitUpdateToggleMoveBoard( self.state, self.move );
            } 
          }, 3000 );
        }
        break;
      case 'START':
        // Display the help
        CitUpdateInstructions( this.state );
        break;
      default: // Do nothing
        break;
    }
    // Check if the game is over 
    this.winner = this.hasWinner();
    var msg;
    if ( this.winner ) {
      switch ( this.winner ) {
        case 1:
          for ( var i = this.board.getPosition() ; i < CitBoard.MAX ; ++i ) {
            this.board.moveRight();
          }
          msg = 'Congratulations,\nyou won!';
          break;
        case 2:
          for ( var i = this.board.getPosition() ; i > 0 ; --i ) {
            this.board.moveLeft();
          }
          msg = 'Oh no, you lost!';
          break;
        case 3:
          msg = 'It\'s a draw! Boring.';
          break;
        default:
          msg = 'Game Over';
          break;
      }
      CitUpdateMsg( this.state, msg );
      CitUpdatePos( this.state, this.board.getPosition() );
      // Return to main menu or if single game refresh the game when finished
      setTimeout( function() { 
        var url = window.location.href;
        url = url.substring( 0, url.lastIndexOf( "/" ) + 1 ) + "../index.html";
        window.location.replace( url );
      }, 5000 );
    }
  }
};
/* Check if there is a winner
 * returns - 0:not finished, 1:player 1, 2:player 2, 3:draw */
CitGame.prototype.hasWinner = function() {
  if ( this.board.getPosition() == this.board.MAX ) return 1;
  if ( this.board.getPosition() == this.board.MIN ) return 2;
  if ( this.player[ 1 ].hasLost() ) {
    if ( this.player[ 2 ].canWin( this.board.getPosition() ) ) {
      while ( this.board.getPosition() > this.board.MIN ) {
        this.player[ 2 ].addMove( 1 );
        this.board.moveLeft();
      }
      return 2;
    } else {
      return 3;
    }
  }
  if ( this.player[ 2 ].hasLost() ) {
    if ( this.player[ 1 ].canWin( this.board.getPosition() ) ) {
      while ( this.board.getPosition() < this.board.MAX ) {
        this.player[ 1 ].addMove( 1 );
        this.board.moveRight();
      }
      return 1;
    } else {
      return 3;
    }
  }
  return 0;
};
CitGame.prototype.run = function() {
  var self = this;
  CitUpdateToggleMoveBoard( this.state, this.move );
  // Start ajax calls to RESTful api
  this.ajax();
  // Allows for keyboard to simulate pes input
  $( 'html' ).keydown( function ( e ) {
    var keyMap = { 37 : 'LEFT', 39 : 'RIGHT', 38 : 'UP', 40 : 'DOWN',
                   13 : 'START', 83 : 'SELECT', 65 : 'A', 66 : 'B' };
    if ( e.which in keyMap ) {
      self.handleInput( keyMap[ e.which ] );
    }
  });
};
/*****************************************************************************/
