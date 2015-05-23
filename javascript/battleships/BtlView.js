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
  // Add message div after board
  body.append( '<div id="msg"></div>' )
  this.msg = $( "#msg" );
  this.x = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J' ];
};
// Add the starting position of the human ships
BtlView.prototype.placeHumanShips = function( ships ) {
  var pos;
  for ( var i = 0 ; i < ships.length ; ++i ) {
    for ( var j = 0 ; j < ships[ i ].getSize() ; ++j ) {
      if ( ships[ i ].getDirection() == '>' ) {
        pos = this.x[ ships[ i ].getX() + j ] + ( ships[ i ].getY() + 1 );
      } else { // 'v'
        pos = this.x[ ships[ i ].getX() ] + ( ships[ i ].getY() + 1 + j );
      }
      this.addShip( 'hum', pos );
    }
  }
};
// Move the aim on the bot board 
BtlView.prototype.setAim = function( pos ) {
  $( ".square" ).removeClass( "selected" );
  $( "#bot" + this.x[ pos[ 0 ] ] + ( pos[ 1 ] + 1 ) ).addClass( "selected" );
}
// Display a message below the boards to the user
BtlView.prototype.showMsg = function( msg ) { this.msg.html( msg ); };
// Update square class
BtlView.prototype.addClass = function( player, pos, cssClass ) { $( "#" + player + pos ).removeClass().addClass( "square " + cssClass ); };
// Wrappers for addClass
BtlView.prototype.addShip = function( player, pos ) { this.addClass( player, pos, "ship" ); };
BtlView.prototype.addHit = function( player, move ) {
  var pos = this.x[ move.getX() ] + ( move.getY() + 1 );
  this.addClass( player, pos, "hit" );
};
BtlView.prototype.addMiss = function( player, move ) {
  var pos = this.x[ move.getX() ] + ( move.getY() + 1 );
  this.addClass( player, pos, "miss" );
};

// Incrememt a single character A->B etc
function inc( c ) {
  return String.fromCharCode( c.charCodeAt( 0 ) + 1 );
}
/*****************************************************************************/
