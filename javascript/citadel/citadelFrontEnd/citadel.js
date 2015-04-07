/******************************************************************************
 * Contains game logic and maintains overall game state                      */
function Citadel() {
  this.board = new CitBoard();
  this.player = { 1 : new CitPlayer( 'Player 1' ),
                  2 : new CitPlayer( 'Player 2' ) };
  this.output = CitOutput();
  this.input  = { 1 : new CitInPES(),
                  2 : new CitInBot() };
}
/* Main game loop */
Citadel.prototype.run() {
  var winner = this.hasWinner();
  while ( 0 == winner ) {
    this.output.showState( this.board.getPosition(),
                           this.player[ 1 ].getPoints(),
                           this.player[ 2 ].getPoints(),
                           this.player[ 1 ].getLastMove(),
                           this.player[ 2 ].getLastMove() );
    this.getMoves();
    winner = this.hasWinner();
  }
  this.output.showState( this.board.getPosition(),
                         this.player[ 1 ].getPoints(),
                         this.player[ 2 ].getPoints(),
                         this.player[ 1 ].getLastMove(),
                         this.player[ 2 ].getLastMove() );
  this.output.showResult( this.hasWinner() );
};
/* Get both players moves */
Citadel.prototype.getMoves() {
  var p1m = this.input[ 1 ].getMove( this.player[ 1 ].getPoints,
                                     this.player[ 2 ].getLastMove() );
  var p2m = this.input[ 2 ].getMove( this.player[ 2 ].getPoints,
                                     this.player[ 1 ].getLastMove() );
  this.player[ 1 ].addMove( p1m );
  this.player[ 2 ].addMove( p2m );
  if ( p1m > p2m ) {
    this.board.moveRight();
  } else if ( p2m > p1m ) {
    this.board.moveLeft();
  } 
}
/* Check if there is a winner
 * returns - 0:not finished, 1:player 1, 2:player 2, 3:draw */
Citadel.prototype.hasWinner() {
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
 * Manipulate the html based on the current game state                       */
function CitOutput() {
  //TODO
}
/* Update the board to the current state */
CitOutput.prototype.showState( pos, p1p, p2p, p1m, p2m ) {
  //TODO
};
/* Display the result once the game has finished */
CitOutput.prototype.showResult( winner ) {
  //TODO
};
/*****************************************************************************/

/******************************************************************************
 * Get user input for the keyboard or pes controller                         */
function CitInPES() {
  //TODO
}
CitInPES.prototype.getMove( points, opLast ) {
  //TODO
};
/*****************************************************************************/

/******************************************************************************
 * Get the user input from the AI bot                                        */
function CitInBot() {
  //TODO
}
CitInBot.prototype.getMove( points, opLast ) {
  //TODO
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
CitBoard.prototype.getPosition() {
  return this.pos;
};
/* If possible move the board position one left */
CitBoard.prototype.moveLeft() {
  if ( this.pos > this.MIN ) {
    this.pos -= 1;
  } 
};
/* If possible move the board position one right */
CitBoard.prototype.moveRight() {
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
CitPlayer.prototype.addMove( move ) {
  if ( this.points < move ) {
    move = this.points;
  }
  this.points -= move;
  this.moves[ this.moves.length ] = move;
};
/* Get the last move played by the player */
CitPlayer.prototype.getLastMove() {
  var move = 0;
  if ( this.moves.length > 0 ) {
    move = this.moves[ this.moves.length - 1 ]
  }
  return move;
};
/* Check if the player has run out of points */
CitPlayer.prototype.hasLost() {
  var lost = false;
  if ( this.points < 1 ) {
    lost = true;
  }
  return lost;
};
/* Check if the player can still win from the current board position */
CitPlayer.prototype.canWin( movesRemaining ) {
  var win = true;
  if ( this.points < movesRemaining ) {
    win = false;
  }
  return win;
};
/* Get the players currents remaining points total */
CitPlayer.prototype.getPoints() {
  return this.points;
};
/* Get the name of the player */
CitPlayer.prototype.getName() {
  return this.name;
};
/*****************************************************************************/
