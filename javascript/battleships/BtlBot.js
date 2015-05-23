/******************************************************************************
 * Computer player logic                                                     */
function BtlBot( bsize ) {
  this.bsize = bsize;
}
BtlBot.prototype.getMove = function( history ) {
  var unique = false;
  var x, y;
  while ( !unique ) {
    x = Math.floor( Math.random() * ( this.bsize - 1 ) );
    y = Math.floor( Math.random() * ( this.bsize - 1 ) );
    unique = true;
    for ( var i = 0 ; i < history.length ; ++i ) {
      if ( ( history[ i ].getX() == x ) && ( history[ i ].getY() == y ) ) {
        unique = false;
      }
    }
  }
  return [ x, y ]; 
}
/*****************************************************************************/
