/******************************************************************************
 * Parent class for maintaing the state of the a single player               */
var Player = function BtlPlayer( name, bsize ) {
  this.name = name;
  this.board = new BtlBoard( bsize );
  this.history = [];
  this.board.positionShips();
}
BtlPlayer.prototype.getName = function() { return this.name; };
BtlPlayer.prototype.getHistory = function() { return this.history; };
BtlPlayer.prototype.getBoard = function() { return this.board; };
BtlPlayer.prototype.repositionShips function() {
  if ( this.history.length == 0 ) {
    this.board.positionShips();
  }
};
// Will return undefined if there is no history
BtlPlayer.prototype.getLastMove = function() {
  return $( this.history ).get( -1 );
};
BtlPlayer.prototype.getNextMove = function() { return false; }; 
/*****************************************************************************/

/******************************************************************************
 * Maintains state of the a single human player                              */
function BtlHuman( name, bsize ) {
  Player.call( this, name, bsize );
}
BtlHuman.prototype = Object.create( Player.prototype );
BtlHuman.prototype.constructor = BtlHuman;
BtlHuman.prototype.getNextMove = function() {
  // Accept arrow inputs to move around the grid
  // Return coordinates of grid when player presses A
  return false;
};
/*****************************************************************************/

/******************************************************************************
 * Maintains state of the a single computer player                           */
function BtlBot( name, bsize ) {
  Player.call( this, name, bsize );
}
BtlBot.prototype = Object.create( Player.prototype );
BtlBot.prototype.constructor = BtlBot;
BtlBot.prototype.getNextMove = function() {
  // Create bot logic here
  return false;
};
/*****************************************************************************/
