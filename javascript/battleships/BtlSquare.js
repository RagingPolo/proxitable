/******************************************************************************
 * Produce the html squares to make up the view of the game                  */
function BtlSquare() {
  this.id = '';
  this.cssClass = '';
  this.content = '';
}
// Rest the square to default values
BtlSquare.prototype.reset = function() {
  this.id = '';
  this.cssClass = '';
  this.content = '';
};
// Add an id to the square
BtlSquare.prototype.addId = function( id ) {
  this.id = id;
};
// Add a class to the square
BtlSquare.prototype.addClass = function( cssClass ) {
  this.cssClass = this.cssClass + ' ' + cssClass;
};
// Add some content to the square
BtlSquare.prototype.addContent = function( content ) {
  this.content += content;
};
// Get the html for a single square
BtlSquare.prototype.getHtml = function() {
  var square = '<div class="square';
  if ( this.cssClass.length > 0  ) {
    square += this.cssClass;
  }
  square += '"';
  if ( this.id.length > 0 ) {
    square += ' id="';
    square += this.id;
    square += '"';
  }
  square += '><div class="content"><div class="centre">';
  square += this.content;
  square += '</div></div></div>\n';
  this.reset();
  return square;
};
/*****************************************************************************/
