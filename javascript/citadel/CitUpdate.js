function CitUpdatePos( state, pos ) {
  // Direction is 1 when going left and -1 when going right
  var direction = pos - state.position;
  console.log( 'p:' + pos + ' d:' + direction );
  if ( direction != 0 ) {
    switch ( pos ) {
      case 0:
        // TODO Display burning castle
        state.army.alpha = 0;
        break;
      case 1:
        CitUpdateArmyPos( state, state.path1_2, direction );
        break;
      case 2:
        if ( 1 == direction ) {
          CitUpdateArmyPos( state, state.path2_3, direction );
        } else {
          CitUpdateArmyPos( state, state.path1_2, direction );
        }
        break;
      case 3:
        if ( 1 == direction ) {
          CitUpdateArmyPos( state, state.path3_4, direction );
        } else {
          CitUpdateArmyPos( state, state.path2_3, direction );
        }
      case 4:
        if ( 1 == direction ) {
          CitUpdateArmyPos( state, state.path4_5, direction );
        } else {
          CitUpdateArmyPos( state, state.path3_4, direction );
        }
      case 5:
        CitUpdateArmyPos( state, state.path4_5, direction );
        break;
      case 6:
        // TODO Display burning castle
        state.army.alpha = 0;
        break;
      default: // Do nothing
        break;
    }
  }
  state.position = pos;
}

/* Move the army sprite */
function CitUpdateArmyPos( state, path, direction ) {
  if ( 1 == direction ) {
    for ( var i = path.length - 1; i >= 0; --i ) {
      state.army.x = path[ i ].x;
      state.army.y = path[ i ].y;
    }
  } else {
    for ( var i = 0; i < path.length; ++i ) {
      state.army.x = path[ i ].x;
      state.army.y = path[ i ].y;
    }
  }
}

/* Display or hide the move board */
function CitUpdateToggleMoveBoard( state, value ) {
  if ( -485 == state.moveBoard.y ) {
    state.moveNumText.setText( value );
    state.boardTween.start();
    state.boardTweenText.start();
  } else if ( 0 == state.moveBoard.y ) {
    state.boardTweenReverse.start();
    state.boardTweenTextReverse.start();
  }
}

/* If the board is displayed update move */
function CitUpdateBid( state, value ) {
  if ( 0 == state.moveBoard.y ) {
    state.moveNumText.setText( value );
  }
}

/* Update players points totals */
function CitUpdatePoints( state, hum, com ) {
  state.humPointsText.setText( hum );
  state.comPointsText.setText( com );
}

/* Display a message to the player */
function CitUpdateMsg( state, msg ) {
  if ( !state.msgTextTweenFadeOut.isRunning ) {
    state.msgText.setText( msg );
    state.msgTextTweenFadeIn.start();
    state.msgBubbleTweenFadeIn.start();
    state.msgTextTweenFadeOut.start();
    state.msgBubbleTweenFadeOut.start();
  }
}

/* Display the 3 part game instructions */
function CitUpdateInstructions( state ) {
  if ( 0 == state.instructions.alpha ) {
    state.instructions.frame = 0;
    state.instructions.alpha = 1;
  } else if ( 0 == state.instructions.frame ) {
    state.instructions.frame = 1;
  } else if ( 1 == state.instructions.frame ) {
    state.instructions.frame = 2;
  } else {
    state.instructions.alpha = 0;
  }
}

/* Check if instructions are currently displayed */
function CitUpdateInstructionsVisible( state ) {
  if ( 1 == state.instructions.alpha ) {
    return true;
  }
  return false;
}
