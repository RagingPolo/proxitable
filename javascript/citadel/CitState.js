var CitState = {};
CitState = function( game ) {
  this.bg                    = null;
  this.cloud1                = null;
  this.cloud2                = null;
  this.cloud3                = null;
  this.humTotal              = null;
  this.comTotal              = null;  
  this.positionMarker        = null;
  this.p1Castle              = null;
  this.p2Castle              = null;
  this.p1Tower               = null;
  this.p2Tower               = null;
  this.army                  = null;
  this.boardTween            = null;
  this.boardTweenText        = null;
  this.msgBubbleTweenFadeIn  = null;
  this.msgBubbleTweenFadeOut = null;
  this.msgTextTweenFadein    = null;
  this.msgTextTweenFadeOut   = null;
  this.direction             = 1;
  //start at pos 3
  this.moveArmyPos           = 994;
  this.arrayOffset           = 0;
  // x,y points of the army positions :TODO add more so it's smoother
  this.point = { 'x': [ 137, 564, 994, 1476, 1760 ],   'y': [ 552, 760, 767, 705, 565 ] };
  this.path = [];
  this.position = 3;
};
CitState.prototype = {
  // Load state assets
  preload: function() {
    this.load.image( 'bg', 'assets/bg.png' );
    this.load.image( 'cloud1', 'assets/cloud1.png' );
    this.load.image( 'cloud2', 'assets/cloud2.png' );
    this.load.image( 'cloud3', 'assets/cloud3.png' );
    this.load.image( 'comTotal', 'assets/comTotal.png' );
    this.load.image( 'humTotal', 'assets/humTotal.png' );
    this.load.image( 'msgBubble', 'assets/msgBubble.png' );
    this.load.image( 'moveBoard', 'assets/moveBoard.png' );
    this.load.image( 'army', 'assets/army.png' );
    this.load.spritesheet( 'positionMarker', 'assets/posInfo.png', 841, 65 );
    this.load.spritesheet( 'castle', 'assets/castles.png', 227, 288  );
    this.load.spritesheet( 'tower', 'assets/towers.png', 80, 142, 2 );
    this.load.spritesheet( 'instructions', 'assets/instructions.png', 1920, 1080 );
  },
  // Place assets and elements in starting postions and create initial state
  create: function() {
    this.bg = this.add.sprite( 0, 0, 'bg' );
    this.cloud1 = this.add.sprite( 640, 358, 'cloud1' );
    this.cloud2 = this.add.sprite( 1436, 189, 'cloud2' );
    this.cloud3 = this.add.sprite( 114, -15, 'cloud3' );
    this.humTotal = this.add.sprite( 20, 20, 'humTotal' );
    this.comTotal = this.add.sprite( 1782, 20, 'comTotal' );
    this.positionMarker = this.add.sprite( 595, 991, 'positionMarker' );
    this.positionMarker.frame = 3;
    this.p1Castle = this.add.sprite( 0, 264, 'castle' );
    this.p1Castle.frame = 1;
    this.p2Castle = this.add.sprite( 1669, 287, 'castle' );
    this.p2Castle.frame = 0;
    this.p1Tower = this.add.sprite( 524, 593, 'tower' );
    this.p1Tower.frame = 1;
    this.p2Tower = this.add.sprite( 1440, 569, 'tower' );
    this.p2Tower.frame = 0;
    this.army = this.add.sprite( 994, 767, 'army' );
    this.army.anchor.set( 0.5 );
    // Setup the move board above the screen
    this.moveBoard = this.add.sprite( 727, -485, 'moveBoard' );
    var moveStyle = { font: "65px Arial", fill: "#ffffff", align: "center" };
    this.moveNumText = this.add.text( 965, -187, "1", moveStyle );
    // Tween the board down
    this.boardTween = this.add.tween( this.moveBoard).to( { y: '+485' }, 500, Phaser.Easing.Linear.None, false );
    this.boardTweenText = this.add.tween( this.moveNumText ).to( { y: '+485' }, 500, Phaser.Easing.Linear.None, false );
    // Reverse the board
    this.boardTweenReverse = this.add.tween( this.moveBoard ).to( { y: '-485' }, 500, Phaser.Easing.Linear.None, false );
    this.boardTweenTextReverse = this.add.tween( this.moveNumText ).to( { y: '-485' }, 500, Phaser.Easing.Linear.None, false );
    // Setup the message bubble and text
    var msgBubble = this.add.sprite( 315, -1, 'msgBubble' );
    msgBubble.alpha = 0;
    var msgStyle = { font: "25px Arial", fill: "#000000", align: "left" };
    this.msgText = this.add.text( 373, 74, "", msgStyle );
    this.msgText.alpha = 0;
    // Fade in tweens
    this.msgBubbleTweenFadeIn = this.add.tween( msgBubble ).to( { alpha: 1 }, 500, Phaser.Easing.Linear.None, false );
    this.msgTextTweenFadeIn = this.add.tween( this.msgText ).to( { alpha: 1 }, 500, Phaser.Easing.Linear.None, false );
    // Fade out tweens
    var delay = 6500;
    this.msgBubbleTweenFadeOut = this.add.tween( msgBubble ).to( { alpha: 0 }, 500, Phaser.Easing.Linear.None, false, delay );
    this.msgTextTweenFadeOut = this.add.tween( this.msgText ).to( { alpha: 0 }, 500, Phaser.Easing.Linear.None, false, delay );
    // Add the points totals
    var totalStyle = { font: "45px Arial", fill: "#ffffff", align: "center" };
    this.humPointsText = this.add.text( 55, 73, "50", totalStyle );
    this.comPointsText = this.add.text( 1815, 73, "50", totalStyle );
    // Display the game instructions
    this.instructions = this.add.sprite( 0, 0, 'instructions' );
    this.plot();
    // Run the game
    var game = new CitGame( this );
    game.run();
    this.run = false;
  },
  // Plots the path of the army between the points
  plot: function () {
    var x = ( 1 / this.game.width ) * 3;
    var j = 0
    for ( var i = 0; i <= 1; i += x ) {
      var px = this.math.catmullRomInterpolation( this.point.x, i );
      var py = this.math.catmullRomInterpolation( this.point.y, i );
      if ( Math.round( px ) == this.moveArmyPos ) this.arrayOffset = j;
      j++;  
      this.path.push( { x: px, y: py } );
    }
  },
  // State game loop
  update: function() {
    // Animate the clouds with different speeds and directions looping round the sides
    this.cloud1.x += 0.05;
    this.cloud2.x -= 0.07;
    this.cloud3.x += 0.06;
    if ( this.cloud1.x > this.world.width ) {
      this.cloud1.x = 0 - this.cloud1.width;
    }
    if ( this.cloud2.x < -this.cloud2.width ) {
      this.cloud2.x = this.cloud.width;
    }
    if ( this.cloud3.x > this.world.width ) {
      this.cloud3.x = 0 - this.cloud3.width;
    }
    if(Math.round(this.army.x) != this.moveArmyPos) {
      this.army.x = this.path[ this.arrayOffset ].x;
      this.army.y = this.path[ this.arrayOffset ].y;
      this.arrayOffset += this.direction;
      if ( this.arrayOffset < 0 ) this.arrayOffset = 0;
      if ( this.arrayOffset >= this.path.length ) this.arrayOffset = this.path.length -1;
    }
  }
} 
