/******************************************************************************
 * Run game and enforce game logic                                           */
function BtlGame( bsize ) {
  this.players = { 'human' : new BtlHuman( 'Player 1', bsize ),
                   'bot' : new BtlBot( 'Player 2', bsize ) };
  this.winner = 0;
}
BtlGame.prototype.run = function() {
  this.showState();
  while ( !this.winner ) {
    // Get human player move
    this.players.human.getNextMove( this.players.bot.getBoard() );
    this.showState();
    if ( !( this.winner = this.hasWinner() ) ) {
      this.players.bot.getNextMove( this.players.human.getBoard() );
      // Add a pause before displaying bot move?
      this.showState();
      this.winner = this.hasWinner();
    }
  }
  this.showWinner();
};
// Check if we have a winner return player number or zero if no winner
BtlGame.prototype.hasWinner = function() {
  if ( this.players.bot.getBoard().isAllSunk() ) {
    return 1;
  }
  if ( this.players.human.getBoard().isAllSunk() ) {
    return 2;
  }
  return 0;
};
// Update the view with the current game state
BtlGame.prototype.showState = function() {
  //TODO
};
BtlGame.prototype.showWinner = function() {
  if ( 1 == this.winner ) {
    //TODO
  } else if ( 2 == this.winner ) {
    //TODO
  }
};
