/******************************************************************************
 * Parent class for maintaing the state of the a single player               */
function BtlPlayer( name, bsize ) {
  this.name = name;
  this.board = new BtlBoard( bsize );
  this.history = [];
  this.board.positionShips();
}
BtlPlayer.prototype.getName = function() { return this.name; };
BtlPlayer.prototype.getHistory = function() { return this.history; };
BtlPlayer.prototype.getBoard = function() { return this.board; };
BtlPlayer.prototype.repositionShips = function() {
  if ( this.history.length == 0 ) {
    this.board.positionShips();
  }
};
// Will return undefined if there is no history
BtlPlayer.prototype.getLastMove = function() {
  return $( this.history ).get( -1 );
};
// Update history
BtlPlayer.prototype.addMove = function( move ) { this.history.push( move ); };
// Check if a move has already been played
BtlPlayer.prototype.alreadyPlayed = function( move ) {
  for ( var i = 0 ; i < this.history.length ; ++i ) {
    if ( move.compare( this.history[ i ] ) ) {
      return true;
    }
  }
  return false;
};
/*****************************************************************************/
