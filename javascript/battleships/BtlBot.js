/******************************************************************************
 * Computer player logic                                                     */
function BtlBot( bsize, easy ) {
  this.bsize = bsize;
  this.easy = easy;
  this.lock = {
    'on': false,
    'x': null, 
    'y': null,
    'direction': {
      'up': 0,
      'down': 0,
      'left': 0,
      'right': 0,
    }
  };
}
// If we get a hit find the direction of the ship and follow it otherwise 
// take random pot shots until we ht again
BtlBot.prototype.getMove = function( history ) {
  var move = null;
  var x, y;
  var last = ( history.length > 0 ) ? history.slice( -1 )[ 0 ] : null;
  if ( this.easy != true ) {
    // If our last random shot hit something turn the lock on
    if ( ( false == this.lock.on ) && ( last != null ) && ( last.isHit() ) ) {
      this.lock.on = true;
      this.lock.x = last.getX();
      this.lock.y = last.getY();
    }
    // If we have a lock start homing in on the ship
    if ( this.lock.on ) {
      // If a direction is set to true we check the last shot
      // if it was a miss we try the next untried direction
      // otherwise we check if the next shot in that direction 
      // is legal and not already played
      // If we have to hits in one direction we whether the ship
      // is horizontal or vertical and can ignore the other
      if ( this.lock.direction.up != null ) {
        if ( last.isHit() ) {
          ++this.lock.direction.up;
          if ( this.lock.direction.up >= 2 ) {
            this.lock.direction.left = null;
            this.lock.direction.right = null;
          }
          x = last.getX();
          y = last.getY() - 1;
          if ( ( y >= 0 ) && ( this.isUnique( x, y, history ) ) ) {
            move = [ x, y ];
          } else {
            this.lock.direction.up = null;
          }
        } else {
          this.lock.direction.up = null;
        }
      }
      if ( ( null == move ) && ( this.lock.direction.down != null ) ) {
        if ( ( 0 == this.lock.direction.down ) || ( last.isHit() ) ) {
          if ( 0 == this.lock.direction.down ) {
            x = this.lock.x;
            y = this.lock.y + 1;
          } else {
            x = last.getX();
            y = last.getY() + 1;
          }
          ++this.lock.direction.down;
          if ( this.lock.direction.down >= 2 ) {
            this.lock.direction.left = null;
            this.lock.direction.right = null;
          }
          if ( ( y < this.bsize ) && ( this.isUnique( x, y, history ) ) ) {
            move = [ x, y ];
          } else {
            this.lock.direction.down = null;
          }
        } else {
          this.lock.direction.down = null;
        }
      } 
      if ( ( null == move ) && ( this.lock.direction.left != null ) ) {
        if ( ( 0 == this.lock.direction.left ) || ( last.isHit() ) ) {
          if ( 0 == this.lock.direction.left ) {
            x = this.lock.x - 1;
            y = this.lock.y;
          } else {
            x = last.getX() - 1;
            y = last.getY();
          }
          ++this.lock.direction.left;
          if ( ( x >= 0 ) && ( this.isUnique( x, y, history ) ) ) {
            move = [ x, y ];
          } else {
            this.lock.direction.left = null;
          }
        } else {
          this.lock.direction.left = null;
        }
      }
      if ( ( null == move ) && ( this.lock.direction.right != null ) ) {
        if ( ( 0 == this.lock.direction.right ) || ( last.isHit() ) ) {
          if ( 0 == this.lock.direction.right ) {
            x = this.lock.x + 1;
            y = this.lock.y;
          } else {
            x = last.getX() + 1;
            y = last.getY();
          }
          ++this.lock.direction.right;
          if ( ( x < this.bsize ) && ( this.isUnique( x, y, history ) ) ) {
            move = [ x, y ];
          } else {
            this.lock.direction.right = null;
          }
        } else {
          this.lock.direction.right = null;
        }
      }
      this.resetLock();
    }
  }
  // We have not generated a move so just fire anywhere
  if ( null == move ) {
    move = this.getRandomMove( history );
  }
  return move;
}
BtlBot.prototype.getRandomMove = function( history ) {
  var unique = false;
  var x, y;
  while ( !unique ) {
    x = Math.floor( Math.random() * this.bsize );
    y = Math.floor( Math.random() * this.bsize );
    unique = this.isUnique( x, y, history );
  }
  return [ x, y ]; 
};
// Check if the proposed move has already been played
BtlBot.prototype.isUnique = function( x, y, history ) {
  for ( var i = 0 ; i < history.length ; ++i ) {
    if ( ( history[ i ].getX() == x ) && ( history[ i ].getY() == y ) ) {
      return false;
    }
  }
  return true; 
};
// Check if the lock on has finished and reset the object if needed
BtlBot.prototype.resetLock = function() {
  if ( ( null == this.lock.direction.up ) &&
       ( null == this.lock.direction.down ) &&
       ( null == this.lock.direction.left ) &&
       ( null == this.lock.direction.right )
     ) {
    this.lock.on = false;
    this.lock.x = null;
    this.lock.y = null;
    this.lock.direction.up = 0;
    this.lock.direction.down = 0;
    this.lock.direction.left = 0;
    this.lock.direction.right = 0;
  }
};
/*****************************************************************************/
