// List of game names, root dirs. Add new games here
// Any new game can be completly self contained as the main menu
// will load the game 'page'. All that is required is the game
// re loads this main menu when complete.
var games = [ { "name":"Our History","path":"history/index.html", "image":"menu\/historyMenu.jpg"}
             ,{ "name":"Battleships","path":"battleships/index.html", "image":"menu\/battleMenu.jpg" }
             ,{ "name":"4 in a Row","path":"connect4/index.html", "image":"menu\/connectMenu.jpg" }
];

// { "name":"Citadel", "path":"citadel/index.html", "image":"menu\/citadelMenu.jpg" },

var selected;
var save = '';

$( document ).ready( function() {
  // Turn the correct PES buttons on
  var pinStat = { "UP": true, "DOWN": true, "LEFT": true, "RIGHT": true,
                  "SELECT": true, "START": true, "A": true, "B": true };
  var code = new Code();
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
  getButton( code );
  // Allows for keyboard to simulate pes input
  $( 'html' ).keydown( function ( e ) {
    var keyMap = { 37 : 'LEFT', 38 : 'UP', 39 : 'RIGHT', 40 : 'DOWN',
                   65 : 'A', 66 : 'B', 13 : 'START', 83 : 'SELECT' };
    if ( e.which in keyMap ) {
      handleInput( keyMap[ e.which ], code );
    }
  });
});

/*
 * Call the PES RESTful api for button presses
 */
function getButton( code ) {
  $.ajax( {
    type: "GET",
    url: "http://10.0.0.1:8080/pressed",
    dataType: "json",
  }).done( function( data, textStatus, jqXHR  ) {
    handleInput( data.button, code );
    // After the request has returned call again
    getButton( code );
  }).fail( function( jqXHR, textStatus, errorThrown ) {
    console.log( 'Button request failed: ' + textStatus );
    // After the request has returned call again
    getButton( code );
  });  
}

/*
 * Handle the PES/keyboard input
 */
function handleInput( button, code ) {
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
  code.next( button );
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


function Code() {
  this.code = ['UP', 'UP', 'DOWN', 'DOWN', 'LEFT', 'RIGHT', 'LEFT', 'RIGHT', 'B', 'A'];
  this.pos = 0;
}
Code.prototype.next = function(next) {
  if (next == this.code[this.pos]) {
    this.pos += 1;
    if (this.pos == this.code.length) {
      save = $( 'body' ).html();
      $( 'body' ).html( '<video id="rickroll" onended="end()"><source src="rickroll.mp4" type="video/mp4"></video>' );
      $( "#rickroll" )[ 0 ].play()
      this.pos = 0;
    }
  } else {
    this.pos = 0;
  }
};
function end() {
  $( 'body' ).html( save );
}
