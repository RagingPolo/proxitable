/******************************************************************************
 * Stores a single move and translates between human coordinates and list idx */
function BtlMove( x, y ) {
  this.x = x;
  this.y = y;
  this.hit = false;
}
BtlMove.prototype.setHit = function( hit ) { this.hit = hit; };
BtlMove.prototype.isHit = function() { return this.hit }
BtlMove.prototype.getX = function() { return this.x }
BtlMove.prototype.getY = function() { return this.y }
BtlMove.prototype.compare = function( move ) {
  if ( move.getX() == this.x ) {
    return move.getY() == this.y;    
  }
  return false;
}
/*****************************************************************************/
// Create a BtlMove object from human coordinates
function genBtlMove( x, y ) {
  LTON = { 'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9 };
  if ( x >= 'A' && x <= 'J' && y >= 1 && y <= 10 ) {
    return new BtlMove( LTON[ x ], y -1 );
  }
  return null;
}
