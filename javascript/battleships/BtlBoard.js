// Undecided if I would prefer to change direction from v & > to 0 & 1
// The former is easier to understnd in the code, the later should be
// quicker to process

/******************************************************************************
 * Maintains state of the a game board                                       */
function BtlBoard( size ) {
  // Adjust size if needed
  if ( size < 6 ) {
    size = 6;
  } else if ( size > 10 ) {
    size = 10;
  }
  this.size = size;
  // Create the ships
  this.ships = [ new BtlShip( 'Battleship', 4 ),
                 new BtlShip( 'Destroyer', 3 ),
                 new BtlShip( 'Gunship', 2 ) ];
  if ( this.size > 7 ) {
    this.ships.push( new BtlShip( 'Submarine', 3 ) );
  }
  if ( this.size == 10 ) {
    this.ships.push( new BtlShip( 'Aircraft Carrier', 5 ) );
  }
  // Generate the board
  this.board = [];
  for ( var i = 0 ; i < this.size ; ++i ) {
    this.board[ i ] = [];
    for ( var j = 0 ; j < this.size ; ++j ) {
      this.board[ i ][ j ] = 0;
    }
  }
}
BtlBoard.prototype.getSize = function() { return this.size; };
BtlBoard.prototype.getShips = function() { return this.ships; };
// Check if all the ships on the board have been sunk
BtlBoard.prototype.isAllSunk = function() {
  var sunk = true;
  $.each( this.ships, function() {
    if ( this.isSunk() == false ) {
      sunk = false;
    }
  });
  return sunk;
};
// Check a players move against the ships on the board
BtlBoard.prototype.takeShot = function( move ) {
  for ( var i = 0 ; i < this.ships.length ; ++i ) {
    if ( this.ships[ i ].isHit( move.getX(), move.getY(), true ) ) {
      return true;
    }
  }
  return false;
};
// Randomly position the availible ships on the board so
// so they are not overlapping each other
BtlBoard.prototype.positionShips = function() {
  var onboard, overlap = true;
  var x, y, d;
  while ( overlap ) {
    // Pick some random ship positions
    for ( var i = 0 ; i < this.ships.length ; ++i ) {
      onboard = false;
      while ( false == onboard ) {
        x = Math.floor( Math.random() * ( this.size - 1 ) );
        y = Math.floor( Math.random() * ( this.size - 1 ) );
        if ( Math.round( Math.random() ) ) {
          d = 'v';
          onboard = ( y + this.ships[ i ].getSize() - 1 ) < this.size;
        } else {
          d = '>';
          onboard = ( x + this.ships[ i ].getSize() - 1 ) < this.size;
        }
      }
      this.ships[ i ].setPosition( x, y, d );
    }
    overlap = false;
    for ( var i = 0 ; i < this.ships.length ; ++i ) {
      if ( overlap ) {
        break;
      }
      for ( var j = 0 ; j < this.ships.length ; ++j ) {
        if ( overlap ) {
          break;
        }
        if ( this.ships[ i ] != this.ships[ j ] ) {
          if ( this.ships[ i ].getDirection() == 'v' ) {
            x = this.ships[ i ].getX();
            for ( y = this.ships[ i ].getY() ;
                  y < this.ships[ i ].getY() + this.ships[ i ].getSize() ;
                  ++y ) {
              if ( ( overlap = this.ships[ j ].isHit( x, y, false ) ) ) {
                break;
              }
            }
          } else { // getDirection() = '>'
            y = this.ships[ i ].getY();
            for ( x = this.ships[ i ].getX() ;
                  x < this.ships[ i ].getX() + this.ships[ i ].getSize() ;
                  ++x ) {
              if ( ( overlap = this.ships[ j ].isHit( x, y, false ) ) ) {
                break;
              }
            }
          }
        }
      }
    }
  }
};
