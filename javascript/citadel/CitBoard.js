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
