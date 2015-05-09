/******************************************************************************
 * Stores a single move and translates between human coordinates and list idx */
NTOL = { 0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J' };
function BtlMove( x, y ) {
  this.x = x;
  this.y = y;
  this.hit = false;
}
BtlMove.prototype.setHit = function( hit ) {
  if ( hit ) {
    this.hit = true;
  } else {
    this.hit = false;
  }
};
BtlMove.prototype.isHit = function() { return this.hit }
BtlMove.prototype.getX = function() { return this.x }
BtlMove.prototype.getY = function() { return this.y }
// Create a BtlMove object from human coordinates
function genBtlMove( x, y ) {
  LTON = { 'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9 };
  if ( x >= 'A' && x <= 'J' && y >= 1 && y <= 10 ) {
    return new BtlMove( LTON[ x ], y -1 );
  }
  return null;
}
function compareMove( a, b ) {
  if ( a.getY() == b.getY() ) {
    return b.getX() - a.getX();
  } else {
    return b.getY() - a.getY();
  }
}
/*****************************************************************************/
