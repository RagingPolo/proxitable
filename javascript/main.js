// List of game names, root dirs. Add new games here
// Any new game can be completly self contained as the main menu
// will load the game 'page'. All that is required is the game
// re loads this main menu when complete.
// TODO Add game icons/images to be used for menu tiles
// TODO Make it look pretty!!!
var games = [ { "name":"Citadel", "path":"citadel/index.html", "image":"menu\/citadelMenu.jpg" }
             ,{ "name":"Our History","path":"history/index.html", "image":"menu\/historyMenu.jpg" }
];

var selected;

$( document ).ready( function() {
  // Turn the correct PES buttons on
  var pinStat = { "UP": false, "DOWN": false, "LEFT": true, "RIGHT": true,
                  "SELECT": false, "START": true, "A": false, "B": false };
  $.ajax( {
    type: "POST",
    url: "http://10.0.0.1:8080/pins",
    contentType: "application/json",
    dataType: "json",
    data: pinStat,
  }).done( function() {
    console.log( 'PES button setup complete' );
  }).fail( function() {
    console.log( 'PES button setup failed' );
  });
  generateMenu();
  getButton();
  // Allows for keyboard to simulate pes input
  $( 'html' ).keydown( function ( e ) {
    var keyMap = { 37 : 'LEFT', 39 : 'RIGHT', 13 : 'START' };
    if ( e.which in keyMap ) {
      handleInput( keyMap[ e.which ] );
    }
  });
});

/*
 * Call the PES RESTful api for button presses
 */
function getButton() {
  $.ajax( {
    type: "GET",
    url: "http://10.0.0.1:8080/pressed",
    dataType: "json",
  }).done( function( data, textStatus, jqXHR  ) {
    handleInput( data.button );
    // After the request has returned call again
    getButton();
  }).fail( function( jqXHR, textStatus, errorThrown ) {
    console.log( 'Button request failed: ' + textStatus );
    // After the request has returned call again
    getButton();
  });  
}

/*
 * Handle the PES/keyboard input
 */
function handleInput( button ) {
  switch( button ) {
    case 'LEFT':
      select( selected -1 );
      break;
    case 'RIGHT':
      select( selected + 1 );
      break;
    case 'START':
      var url = window.location.href;
      url = url.substring( 0, url.lastIndexOf( "/" ) + 1 ) + games[ selected ].path;
      window.location.replace( url );
      break;
    default:
      // Do nothing
      break;
  }
}

/*
 * Build a tile based menu from the listed games before calling on the 
 * PES api to let the user use the menu
 */ 
function generateMenu() {
  $.each( games, function( idx, game ) {
    var tile = '<div id="' + idx + '" class="tile unselected"><div class="content" style="background-image: url(\''+ game.image +'\');"></div><div class="caret">></div><div class="center">' + game.name + '</div></div>';
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
