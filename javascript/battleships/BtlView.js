/******************************************************************************
 * Generate the html view and provide methods to modify it                   */
function BtlView( size ) {
  var x = 'A';
  var square = new BtlSquare();
  var body = $( "body" );
  // Create top row
  body.append( square.getHtml() ).append( square.getHtml() );
  for ( var i = 0 ; i < size ; ++i ) {
    square.addContent( x );
    square.addClass( "axis" ); 
    body.append( square.getHtml() );
    x = inc( x );
  }
  body.append( square.getHtml() ).append( square.getHtml() );
  x = 'A';
  for ( var i = 0 ; i < size ; ++i ) {
    square.addContent( x );
    square.addClass( "axis" ); 
    body.append( square.getHtml() );
    x = inc( x );
  }
  body.append( square.getHtml() );
  // Create the actual grid
  for ( var i = 0 ; i < size ; ++i ) {
    body.append( square.getHtml() );
    square.addClass( "axis" );
    square.addContent( i + 1 );
    body.append( square.getHtml() );
    x = 'A';
    for ( var j = 0 ; j < size ; ++j ) {
      square.addClass( "water" ); 
      square.addId( "hum" + x + ( i + 1 ) );
      body.append( square.getHtml() );
      x = inc( x );
    }
    body.append( square.getHtml() );
    square.addClass( "axis" );
    square.addContent( i + 1 );
    body.append( square.getHtml() );
    x = 'A';
    for ( var j = 0 ; j < size ; ++j ) {
      square.addClass( "water" ); 
      square.addId( "bot" + x + ( i + 1 ) );
      body.append( square.getHtml() );
      x = inc( x );
    }
    body.append( square.getHtml() );
  }
};
// Update the board for both players
BtlView.prototype.updateGrid = function( hum, bot ) {

};
// Update square class
function gridAddClass( player, pos, cssClass ) {
  $( "#" + player + pos ).removeClass().addClass( "square " + cssClass );
}
// Wrappers for addClass
function gridAddShip( player, pos ) { gridAddClass( player, pos, "ship" ); }
function gridAddHit( player, pos ) { gridAddClass( player, pos, "hit" ); }
function gridAddMiss( player, pos ) { gridAddClass( player, pos, "miss" ); }

// Incrememt a single character A->B etc
function inc( c ) {
  return String.fromCharCode( c.charCodeAt( 0 ) + 1 );
}
/*****************************************************************************/
