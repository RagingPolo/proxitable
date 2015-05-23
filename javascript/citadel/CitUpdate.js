function CitUpdatePos( state, pos ) {
  // Direction is 1 when going right and -1 when going left
  state.direction = pos - state.position;
  // Update bottom display
  state.positionMarker.frame = pos;
  // Move the army along
  if( 0 == pos ) {
    state.p1Castle.frame = 2;
    state.army.alpha = 0;
  }
  else if ( 6 == pos ) {
    state.p2Castle.frame = 3;
    state.army.alpha = 0;
  }
  else {
    state.moveArmyPos = state.point.x[ pos - 1 ];
    state.position = pos;
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

/* Check if the move board is visible to the player  */
function CitUpdateBoardVisible( state ) {
  if ( 0 == state.moveBoard.y ) {
    return true;
  }
  return false;
}

/* If the board is displayed update move */
function CitUpdateBid( state, value ) {
  if ( CitUpdateBoardVisible( state )  ) {
    state.moveNumText.setText( value );
  }
}

/* Update players points totals */
function CitUpdatePoints( state, hum, com ) {
  //if less than 10 pad with leading a space
  if ( hum < 10 ) state.humPointsText.setText( " " + hum );
  else state.humPointsText.setText( hum );

  if ( com < 10 ) state.comPointsText.setText( " " + com );
  else state.comPointsText.setText( com );
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
