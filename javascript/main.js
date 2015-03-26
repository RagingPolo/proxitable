// List of game names, root dirs. Add new games here
// Any new game can be completly self contained as the main menu
// will load the game 'page'. All that is required is the game
// re loads this main menu when complete.
// TODO Add game icons/images to be used for menu tiles
var games = [
   { name:"Citadel", path:"citadel/main.html" }
  ,{ name:"Battleships", path:"battleships/main.html" }
  ,{ name:"Our History", path:"history/main.html" }
];
var selected;

$( document ).ready( function() {
  generateMenu();
  // TODO Make ajax call to PES api for button presses
  // TODO When start/enter is pressed load the file at the selected games path
  // Allows for keyboard to simulate pes input
  $( 'html' ).keydown( function ( e ) {
    switch ( e.which ) {
      case 37: // LEFT
        select( selected - 1 ); 
        break;
      case 39: // RIGHT
        select( selected + 1 );
        break;
      default:
        // Do Nothing
        break;
    }
  });
});

/*
 * Build a tile based menu from the listed games before calling on the 
 * PES api to let the user use the menu
 */ 
function generateMenu() {
  $.each( games, function( idx, game ) {
    var tile = '<div id="' + idx + '" class="tile unselected"><div class="content"><div class="center">' + game[ 'name' ] + '</div></div></div>';
    $( '#menu' ).append( tile );                 
  });
  select( 0 );
};

/*
 * Change the visual appearance of a selected tile
 */
function select( id ) {
  if ( id == -1 ) id = games.length - 1;
  if ( id == games.length ) id = 0;
  $.each( new Array( games.length), function( n ) {
    $( '#' + n ).removeClass( 'selected' ).addClass( 'unselected' );
  }); 
  $( '#' + id ).removeClass( 'unselected' ).addClass( 'selected' );
  selected = id;
};
