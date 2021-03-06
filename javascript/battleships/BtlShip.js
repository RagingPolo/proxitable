/******************************************************************************
 * Maintains state of a single ship                                          */
function BtlShip( name, size, img ) {
  this.name = name;
  this.size = size;
  this.img = img;
  this.x = null;
  this.y = null;
  this.dir - null;
  this.hits = [];
  for ( var i = 0 ; i < size ; ++i ) {
    this.hits.push( 0 );
  }
}
BtlShip.prototype.getName = function() { return this.name; };
BtlShip.prototype.getDirection = function() { return this.dir; };
BtlShip.prototype.getX = function() { return this.x; };
BtlShip.prototype.getY = function() { return this.y; };
BtlShip.prototype.getSize = function() { return this.size; };
// Record the position of the ship on the board, it is assumed that this
// position fits inside the current board, the checking should be done
// by the callee
BtlShip.prototype.setPosition = function( x, y, direction ) {
  if ( $.inArray( direction, [ 'v', '>' ] ) > -1 ) {
     this.x = x;
     this.y = y;
     this.dir = direction;
  }
};
BtlShip.prototype.setHit = function( pos ) {
  if ( pos < this.size ) {
    this.hits[ pos ] = 1;
  }
};
// Check if part of the ship is at x,y
// If shot is true it will be recorded as a hit
BtlShip.prototype.isHit = function( x, y, shot ) {
  if ( this.x != null && this.y != null && this.dir != null ) {
    // Vertical ship
    if ( this.dir == 'v' && this.x == x ) {
      if ( y >= this.y && y < ( this.y + this.size ) ) {
        if ( shot ) this.hits[ y - this.y ] = 1;
        return true;
      }
    // Horizontal ship
    } else if ( this.dir == '>' && this.y == y ) {
      if ( x >= this.x && x < ( this.x + this.size ) ) {
        if ( shot ) this.hits[ x - this.x ] = 1;
        return true;
      }
    }
  }
  return false;
};
// If part of the ship is at x,y return the correct img
BtlShip.prototype.getImg = function( x, y ) {
  if ( this.x != null && this.y != null && this.dir != null ) {
    // Vertical ship
    if ( this.dir == 'v' && this.x == x ) {
      if ( y >= this.y && y < ( this.y + this.size ) ) {
        return this.img + ( y - this.y ) + '.png';
      }
    // Horizontal ship
    } else if ( this.dir == '>' && this.y == y ) {
      if ( x >= this.x && x < ( this.x + this.size ) ) {
        return this.img + ( x - this.x ) + '.png';
      }
    }
  }
  return false;
};
// Check if the shit has been sunk
BtlShip.prototype.isSunk = function() {
  var sunk = 0;
  for ( var i = 0 ; i < this.hits.length ; ++i ) {
    sunk += this.hits[ i ];
  }
  if ( sunk == this.size ) return true;
  return false;
};
/*****************************************************************************/
