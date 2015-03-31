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
