/******************************************************************************
 * Manipulate the view of the game in the browser window                     */
function ConView() {
  this.width = 7;
  this.height = 6;
  // Build the starting html
  $( 'body' ).html( '<div class="board"></div><div id="msg"></div>' );
  var div = $( '.board' );
  for ( var c = 0 ; c < this.width ; ++c ) {
    if ( 0 == c ) {
      div.append( '<div class="square-border"></div>' ); 
    }
    div.append( '<div class="square drop" id="drop' + c + '"></div>' ); 
    if ( ( this.width - 1 ) == c ) {
      div.append( '<div class="square-border"></div>' ); 
    }
  }
  for ( var r = this.height ; r > 0 ; --r ) {
    for ( var c = 0 ; c < this.width ; ++c ) {
      if ( 0 == c ) {
        div.append( '<div class="square-border grid-border"></div>' ); 
      }
      div.append( '<div class="square grid" id="' + c + '-' + ( r - 1 ) + '"></div>' ); 
      if ( ( this.width - 1 ) == c ) {
        div.append( '<div class="square-border grid-border"></div>' ); 
      }
    }
  }
  $( '#msg' ).hide();
}
// Move the bouncing arrow
ConView.prototype.hideSelected = function() {
  $( '.drop' ).removeClass( 'selected bounce' );
};
ConView.prototype.setSelected = function( selected ) {
  this.hideSelected();
  $( '#drop' + selected ).addClass( 'selected bounce' );
};
// Drop a piece into the grid
ConView.prototype.drop = function( id, player ) {
  var colour = ( 1 == player ) ? 'yellow' : 'red';
  $( '#' + id ).css( 'background-color', colour );
};
// Display a message
ConView.prototype.showMsg = function( msg, width, height ) {
  if ( undefined === width ) {
    width = 500;
  }
  if ( undefined === height ) {
    height = 100;
  }
  var div = $( '#msg' )
  div.css( 'width', width + 'px' );
  div.css( 'height', height + 'px' );
  div.css( 'margin-left', '-' + ( width / 2 ) + 'px' );
  div.css( 'margin-top', '-' + ( height / 2 ) + 'px' );
  div.html( msg ).show();
}
ConView.prototype.fadeMsg = function( time, callback, args ) {
  if ( undefined === callback ) {
    $( '#msg' ).fadeOut( time );
  } else {
    $( '#msg' ).fadeOut( time, callback( args ) );
  }
}
ConView.prototype.hideMsg = function() {
  $( '#msg' ).hide();
};
