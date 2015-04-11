$( document ).ready( function() {
  var game = new Citadel();
  game.run();
});

/******************************************************************************
 * Contains game logic and maintains overall game state                      */
function Citadel() {
  this.winner = 0;
  this.help   = 1;
  this.move   = 1;
  this.board  = new CitBoard();
  this.bot    = new CitInBot();
  this.player = { 1 : new CitPlayer( 'Player 1' ),
                  2 : new CitPlayer( 'Player 2' ) };
  this.phaser = new Phaser.Game( '100', '100', Phaser.AUTO, '<html>', {}, true ); 
  this.phaser.state.add( 'View', CitPhaser.View );
}
Citadel.prototype.run = function() {
  this.phaser.state.start( 'View' );
  CitPhaser.update.toggleMoveBoard();
  // Start ajax calls to RESTful api
  this.ajax();
  // Allows for keyboard to simulate pes input
  $( 'html' ).keydown( function ( e ) {
    var keyMap = { 37 : 'LEFT', 39 : 'RIGHT', 38 : 'UP', 40 : 'DOWN',
                   13 : 'START', 83 : 'SELECT', 65 : 'A', 66 : 'B' };
    if ( e.which in keyMap ) {
      this.handleInput( keyMap[ e.which ] );
    }
  });
};
Citadel.prototype.ajax = function() {
  $.ajax( {
    type: "GET",
    url: "http://127.0.0.1:8080/pressed",
    dataType: "json",
  }).done( function( data, textStatus, jqXHR  ) {
    this.handleInput( data[ 'button' ] );
    // After the request has returned call again
    this.ajax();
  }).fail( function( jqXHR, textStatus, errorThrown ) {
    console.log( 'Button request failed: ' + textStatus );
    // After the request has returned call again
    this.ajax();
  });  
};
Citadel.prototype.handleInput = function( button ) {
  switch ( button ) {
    case 'UP':
      // Increase the propsed move by one
      if ( !help ) {
        if ( this.move < this.player[ 1 ].getPoints() ) {
          ++this.move;
          CitPhaser.update.bid( this.move );
        }
      }
      break;
    case 'DOWN':
      // Decrease the proposed move by one
      if ( !help ) {
        if ( this.move > 0 ) {
          --this.move;
          CitPhaser.update.bid( this.move );
        }
      }
      break;
    case 'LEFT':
      // Do nothing
      break;
    case 'RIGHT':
      // Do nothing
      break;
    case 'A':
      if ( !help ) {       
        CitPhaser.update.toggleMoveBoard();
        // Play the current amount of points and get a move from the bot
        this.player[ 1 ].addMove( this.move );
        this.player[ 2 ].addMove( this.bot.getMove( this.player[ 2 ].getPoints(),
                                                    this.player[ 1 ].getLastMove() ) );
        // Perform the move
        if ( this.player[ 1 ].getLastMove() > this.player[ 2 ].getLastMove() ) {
          this.board.moveRight();
        } else if ( this.player[ 1 ].getLastMove() < this.player[ 2 ].getLastMove() ) {
          this.board.moveLeft();
        }
        // Update the view
        CitPhaser.update.position( this.board.getPosition() );
        CitPhaser.update.points( this.player[ 1 ].getPoints(), this.player[ 2 ].getPoints() );
        // TODO implement a flag that is turned on here and turned off after a preset delay
        // while this flag is on all non help button presses are ignored
        // when the falg timesout call: CitPhaser.update.toggleMoveBoard();
      }
      break;
    case 'B':
      // Do nothing
      break;
    case 'START':
      // Display the help
      CitPhaser.update.instructions();
      ++this.help;
      if ( this.help == 4 ) {
        this.help = 0;
      }
      break;
    case 'SELECT':
      // Do nothing
      break
    default:
      break;
  }
  // Check if the game is over 
  var winner = this.hasWinner();
  var msg;
  if ( winner ) {
    switch ( winner ) {
      case 1:
        msg = 'Congratulations, you won!';
        break;
      case 2:
        msg = 'Oh no, you lost!';
        break;
      case 3:
        msg = 'It\'s a draw! Boring.';
        break;
      default:
        msg = 'Game Over';
        break;
    }
    CitPhaser.update.message( msg );
    // TODO end the game, return to main menu
  }
};
/* Check if there is a winner
 * returns - 0:not finished, 1:player 1, 2:player 2, 3:draw */
Citadel.prototype.hasWinner = function() {
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
/*****************************************************************************/

/******************************************************************************
 * Get the user input from the AI bot                                        */
function CitInBot() {
  this.bot = new CitBot()
}
CitInBot.prototype.getMove = function( points, opLast ) {
  return this.bot.getMove( points, opLast );
};
/*****************************************************************************/

/******************************************************************************
 * Maintains state of the citadel game board, board consists of 7 positions  */
function CitBoard() {
  this.MIN = 0; // Lowest board position
  this.MAX = 6; // Highest board position
  this.pos = 3; // Starting position
}
/* Get the current board position */
CitBoard.prototype.getPosition = function() {
  return this.pos;
};
/* If possible move the board position one left */
CitBoard.prototype.moveLeft = function() {
  if ( this.pos > this.MIN ) {
    this.pos -= 1;
  } 
};
/* If possible move the board position one right */
CitBoard.prototype.moveRight = function() {
  if ( this.pos < this.MAX ) {
    this.pos += 1;
  }
};
/*****************************************************************************/

/******************************************************************************
 * Maintains state of a single player in the citadel game                    */
function CitPlayer( name ) {
  this.points = 50;
  this.moves  = [];
  this.name = name;
};
/* Add the next move to the players move history and adjust the remaining
 * points accordingly. It is up to the input method to ensure that the move
 * is a valid move */
CitPlayer.prototype.addMove = function( move ) {
  if ( this.points < move ) {
    move = this.points;
  }
  this.points -= move;
  this.moves[ this.moves.length ] = move;
};
/* Get the last move played by the player */
CitPlayer.prototype.getLastMove = function() {
  var move = 0;
  if ( this.moves.length > 0 ) {
    move = this.moves[ this.moves.length - 1 ]
  }
  return move;
};
/* Check if the player has run out of points */
CitPlayer.prototype.hasLost = function() {
  var lost = false;
  if ( this.points < 1 ) {
    lost = true;
  }
  return lost;
};
/* Check if the player can still win from the current board position */
CitPlayer.prototype.canWin = function( movesRemaining ) {
  var win = true;
  if ( this.points < movesRemaining ) {
    win = false;
  }
  return win;
};
/* Get the players currents remaining points total */
CitPlayer.prototype.getPoints = function() {
  return this.points;
};
/* Get the name of the player */
CitPlayer.prototype.getName = function() {
  return this.name;
};
/*****************************************************************************/
