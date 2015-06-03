/******************************************************************************
 * Maintains state of the a game board                                       */
function ConBoard() {
  this.width = 7;
  this.height = 6;
  // Build the empty game board
  this.board = [];
  for ( var i = 0 ; i < this.width ; ++i ) {
    this.board[ i ] = [];
    for ( var j = 0 ; j < this.height ; ++j ) {
      this.board[ i ][ j ] = 0; 
    }
  }
}
//
ConBoard.prototype.getWidth = function() { return this.width; }; 
ConBoard.prototype.getHeight = function() { return this.height; }; 
// Drop a piece into the board
ConBoard.prototype.drop = function( col, player ) {
  if ( ( col > -1 ) && ( ( col - 1 ) < this.width ) &&
       ( ( 1 == player ) || ( 2 == player ) ) ) {
    for ( var i = 0 ; i < this.height ; ++i ) {
      if ( 0 == this.board[ col ][ i ] ) {
        this.board[ col ][ i ] = player;
        return col + '-' + i;
      }
    }
  }
  return false;
};
// Check if there is a winner
ConBoard.prototype.winner = function() {
  var line = 0;
  var player = 0;
  // Check vertically
  for ( var c = 0 ; c < this.width ; ++c ) {
    for ( var r = 0 ; r < this.height ; ++r ) {
      if ( 0 == this.board[ c ][ r ] ) {
        // There are no more pieces in the column
        player = 0;
        line = 0;
        break;
      }
      if ( 0 == line ) {
        // Record the player attempting a line
        player = this.board[ c ][ r ];
      } else {
        if ( player != this.board[ c ][ r ] ) {
          // It's the other player so reset the player and line counter
          player = this.board[ c ][ r ];
          line = 0;
        }
      }
      // increment the line counter and if it equals four we have a winner
      ++line;
      if ( 4 == line ) {
        return player;
      }
    }
  }
  // We didn't find a winner so check horizontally
  line = 0;
  player = 0;
  for ( var r = 0 ; r < this.height ; ++r ) {
    for ( var c = 0 ; c < this.width ; ++c ) {
      if ( player != this.board[ c ][ r ] ) {
        player = this.board[ c ][ r ];
        line = 0;
      }
      // if player is currently an actual player increment
      // line, if line reaches 4 we have a winner
      if ( player != 0 ) {
        ++line;
      }
      if ( 4 == line ) {
        return player;
      }
    }
  }
  // Still no winner so check diagonally
  for ( var c = 0 ; c < ( this.width - 3 ) ; ++c ) {
    for ( var r = 3 ; r < this.height ; ++r ) {
      if ( ( player = this.match( [ this.board[ c ][ r ],
                                    this.board[ c + 1 ][ r - 1 ], 
                                    this.board[ c + 2 ][ r - 2 ], 
                                    this.board[ c + 3 ][ r - 3 ] ]
         ) ) ) {
        return player;                              
      } 
    }
  }
  for ( var c = 0 ; c < ( this.width - 3 ) ; ++c ) {
    for ( var r = 0 ; r < ( this.height - 3 ) ; ++ r ) {
      if ( ( player = this.match( [ this.board[ c ][ r ],
                                    this.board[ c + 1 ][ r + 1 ], 
                                    this.board[ c + 2 ][ r + 2 ], 
                                    this.board[ c + 3 ][ r + 3 ] ]
         ) ) ) {
        return player;                              
      } 
    }
  }
  // Neither player has won yet
  return 0;
};
// Check if the board is full
ConBoard.prototype.full = function() {
  for ( var c = 0 ; c < this.width ; ++c ) {
    for ( var r = 0 ; r < this.height ; ++r ) {
      if ( 0 == this.board[ c ][ r ] ) {
        return false;
      }
    }
  }
  return true;
};
// Compare 4 values and return the value if they all match
ConBoard.prototype.match = function( list ) {
  var value = 0;
  if ( list.length == 4 ) {
    value = list[ 0 ];
    for ( var i = 1 ; i < list.length ; ++i ) {
      if ( value != list[ i ] ) {
        value = 0;
        break;
      }
    }
  }
  return value;
}
