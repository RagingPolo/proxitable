/* AI player for citadel */
function CitBot() {
  this.pos          = 3;
  this.opPoints     = 50;
  this.startPoints  = 50;
  this.last         = 0;
}
/* Calculate the next AI move */
CitBot.prototype.getMove = function( points, opLast ) {
  var move = 0;
  var min;
  var max;
  // Update recorded state
  this.opPoints -= opLast;
  if ( this.last != 0 ) {
    if ( last > opLast ) {
      ++this.pos;
    } else if ( last < opLast ) {
      --this.pos;
    }
  }
  // Generate move based on state information
  switch ( this.pos ) {
    case 1:
      if ( points < this.opPoints ) move = points;
      else if ( ( points * ( 1/4 ) ) > this.opPoints ) move = points * ( 1/4 );
      else if ( ( points * ( 1/3 ) ) > this.opPoints ) move = points * ( 1/3 );
      else if ( ( points * ( 2/4 ) ) > this.opPoints ) move = points * ( 2/4 );
      else if ( ( points * ( 2/3 ) ) > this.opPoints ) move = points * ( 2/3 );
      else if ( ( points * ( 3/4 ) ) > this.opPoints ) move = points * ( 3/4 );
      else move = this.random( points * ( 2/3 ), max = points * ( 3/4 ) );
      break;
    case 2:
      if ( ( points * ( 2/3 ) ) < this.opPoints ) move = points * ( 1/3 );
      else if ( ( points * ( 3/4 ) ) < this.opPoints ) move = points * ( 1/4 );
      else if ( points < this.opPoints ) move = this.random( points * ( 2/4 ), points * ( 3/4 ) );
      else if ( points > this.opPoints ) move = this.random( points * ( 1/4 ), points * ( 2/4 ) );
      else move = this.random( points * ( 1/4 ), points * ( 1/3 ) ); 
      break;
    case 3:
      max = ( points > 10 ) ? 10 : points ;
      move = ( Math.random() * max ) + 1;
      break;
    case 4:
      if ( ( points * ( 1/3 ) ) > this.opPoints ) move = points * ( 2/3 );
      else if ( ( points * ( 1/4 ) ) > this.opPoints ) move = points * ( 3/4 );
      else if ( points > this.opPoints ) move = this.random( points * ( 2/4 ), points * ( 3/4 ) );
      else if ( points < this.opPoints ) move = this.random( points * ( 1/4 ), points * ( 2/4 ) );
      else move = this.random( points * ( 1/4 ), points * ( 1/3 ) ); 
      break;
    case 5:
      if ( points > this.opPoints ) move = this.opPoints + 1;		
      else if ( points < ( this.opPoints * ( 1/4 ) ) ) move = points * ( 1/4 );
      else if ( points < ( this.opPoints * ( 1/3 ) ) ) move = points * ( 1/3 );
      else if ( ( points * ( 3/4 ) ) < ( this.opPoints * ( 2/3 ) ) ) move = points * ( 2/3 );
      else move = this.random( points * ( 1/4 ), points * ( 1/3 ) ); 
      break;
    default:
      break;
  }
  // Ensure the move is an integer
  move =  Math.floor( move );
  if ( move == 0 ) {
    move = 1;
  }
  console.log(this.pos + ' ' + move);
  return move;
};
/* Generate a random move between the min and max values */
CitBot.prototype.random = function( min, max ) {
  return ( Math.random() * ( min + max ) ) + min;
}
