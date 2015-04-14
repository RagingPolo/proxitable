var CitPhaser = {};
//holds all the view items and creates moving background
CitPhaser.View = function ( game ) {

  this.cloud1 = null;
  this.cloud2 = null;
  this.cloud3 = null; 

  CitPhaser.positionMarker = null;
  CitPhaser.p1Castle = null;
  CitPhaser.p2Castle = null;
  CitPhaser.p1Tower = null;
  CitPhaser.p2Tower = null;
  CitPhaser.army = null;
  //points of the army positions;
  CitPhaser.point1_2 = {
    'x': [ 137, 564 ],
    'y': [ 552, 760 ]
  };
  CitPhaser.point2_3 = {
    'x': [ 564, 994 ],
    'y': [ 760, 767 ]
  };
  CitPhaser.point3_4 = {
    'x': [ 994, 1476 ],
    'y': [ 767, 705 ]
  };
  CitPhaser.point4_5 = {
    'x': [ 1476, 1760 ],
    'y': [ 705, 565 ]
  };

  CitPhaser.path1_2 = [];
  CitPhaser.path2_3 = [];
  CitPhaser.path3_4 = [];
  CitPhaser.path4_5 = [];

  CitPhaser.boardTween = null;
  CitPhaser.boardTweenText = null;
  CitPhaser.messageBubbleTweenFadeIn = null;
  CitPhaser.messageTextTweenFadeIn = null;
  CitPhaser.messageBubbleTweenFadeOut = null;
  CitPhaser.messageTextTweenFadeOut = null;

  CitPhaser.humPointsText = null;
  CitPhaser.comPointsText = null;
  CitPhaser.moveNumText = null;
  CitPhaser.messageText = null;
  CitPhaser.moveBoard = null;

  CitPhaser.position = 3;
};
CitPhaser.View.prototype = {
  preload: function() {
    this.load.image( 'bg', 'assets/bg.png' );
    this.load.spritesheet( 'positionMarker', 'assets/posInfo.png', 841, 65 );
    this.load.spritesheet( 'castle', 'assets/castles.png', 227, 288 );
    this.load.spritesheet( 'tower', 'assets/towers.png', 80, 142, 2 );
    this.load.spritesheet( 'instructions', 'assets/instructions.png', 1920, 1080 );
    this.load.image( 'cloud1', 'assets/cloud1.png' );            
    this.load.image( 'cloud2', 'assets/cloud2.png' );            
    this.load.image( 'cloud3', 'assets/cloud3.png' ); 
    this.load.image( 'comTotal', 'assets/comTotal.png' );
    this.load.image( 'humTotal', 'assets/humTotal.png' );
    this.load.image( 'messageBubble', 'assets/messageBubble.png' );
    this.load.image( 'moveBoard', 'assets/moveBoard.png' );
    this.load.image( 'army', 'assets/army.png' );           
  },
  create: function() {

    console.log( 'Create called' );

    var bg = this.add.sprite( 0, 0, 'bg' );
    this.cloud1 = this.add.sprite( 640, 358, 'cloud1' );
    this.cloud2 = this.add.sprite( 1436, 189, 'cloud2' );
    this.cloud3 = this.add.sprite( 114,-15, 'cloud3' );
    var humTotal = this.add.sprite( 20, 20, 'humTotal' );
    var comTotal = this.add.sprite( 1781, 20, 'comTotal' );
    CitPhaser.positionMarker = this.add.sprite( 595, 991, 'positionMarker' );
    CitPhaser.positionMarker.frame = 3;
    CitPhaser.p1Castle = this.add.sprite( 0, 264, 'castle' );
    CitPhaser.p1Castle.frame = 1;
    CitPhaser.p2Castle = this.add.sprite( 1669, 287, 'castle' );
    CitPhaser.p1Tower = this.add.sprite( 524, 593, 'tower' );
    CitPhaser.p1Tower.frame = 1;
    CitPhaser.p2Tower = this.add.sprite( 1440, 569, 'tower' );
    CitPhaser.army = this.add.sprite( 994, 767, 'army' );
    CitPhaser.army.anchor.set( 0.5 );
    //setup move board above screen
    CitPhaser.moveBoard = this.add.sprite( 727, -485, 'moveBoard' );
    var moveStyle = { font: "65px Arial", fill: "#ffffff", align: "center" };
    CitPhaser.moveNumText = this.add.text( 965, -187, "1", moveStyle );
    //tween the board down
    CitPhaser.boardTween = this.add.tween( CitPhaser.moveBoard ).to( { y: '+485' }, 500, Phaser.Easing.Linear.None, false );
    CitPhaser.boardTweenText = this.add.tween( CitPhaser.moveNumText ).to( { y: '+485' }, 500, Phaser.Easing.Linear.None, false );
    //reverse the board
    CitPhaser.boardTweenReverse = this.add.tween( CitPhaser.moveBoard ).to( { y: '-485' }, 500, Phaser.Easing.Linear.None, false );
    //setup message text and bubble
    var messageBubble = this.add.sprite( 315, -1, 'messageBubble' );
    var messageStyle = { font: "25px Arial", fill: "#000000", align: "left" };
    CitPhaser.messageText = this.add.text( 373, 74, "", messageStyle );
    messageBubble.alpha = 0;
    CitPhaser.messageText.alpha = 0;
    //fade in tweens
    CitPhaser.messageBubbleTweenFadeIn = this.add.tween( messageBubble ).to( { alpha: 1 }, 500,Phaser.Easing.Linear.None, false );
    CitPhaser.messageTextTweenFadeIn = this.add.tween( CitPhaser.messageText ).to( { alpha: 1 }, 500,Phaser.Easing.Linear.None, false );
    //fade out  tweens - delay ( 6500 - 500 ) is how long the message will stay for
    CitPhaser.messageBubbleTweenFadeOut = this.add.tween( messageBubble ).to( { alpha: 0 }, 500, Phaser.Easing.Linear.None, false, 6500 );
    CitPhaser.messageTextTweenFadeOut = this.add.tween( CitPhaser.messageText ).to( { alpha: 0 }, 500, Phaser.Easing.Linear.None, false, 6500 );
    //add point totals
    var totalStyle = { font: "45px Arial", fill: "#ffffff", align: "center" };
    CitPhaser.humPointsText = this.add.text( 55, 73, "50", totalStyle );
    CitPhaser.comPointsText = this.add.text( 1815, 73, "50", totalStyle );
    // display instructions
    CitPhaser.instructions = this.add.sprite( 0, 0, 'instructions' );
    this.plot();
  },
  //plots the path of the army between the points (x4 )
  plot: function () {
    var x = 1 / this.game.width;
    for ( var i = 0; i <= 1; i += x ) {
      var px = this.math.catmullRomInterpolation( CitPhaser.point1_2.x, i );
      var py = this.math.catmullRomInterpolation( CitPhaser.point1_2.y, i );
      CitPhaser.path1_2.push( { x: px, y: py } );
    }
    for ( var i = 0; i <= 1; i += x ) {
      var px = this.math.catmullRomInterpolation( CitPhaser.point2_3.x, i );
      var py = this.math.catmullRomInterpolation( CitPhaser.point2_3.y, i );
      CitPhaser.path2_3.push( { x: px, y: py } );
    }
    for ( var i = 0; i <= 1; i += x ) {
      var px = this.math.catmullRomInterpolation( CitPhaser.point3_4.x, i );
      var py = this.math.catmullRomInterpolation( CitPhaser.point3_4.y, i );
      CitPhaser.path3_4.push( { x: px, y: py } );
    }
    for ( var i = 0; i <= 1; i += x ) {
      var px = this.math.catmullRomInterpolation( CitPhaser.point4_5.x, i );
      var py = this.math.catmullRomInterpolation( CitPhaser.point4_5.y, i );
      CitPhaser.path4_5.push( { x: px, y: py } );
    }
  },
  update: function () {
    //animated clouds!
    //varied speeds and direction
    this.cloud1.x +=0.05;
    this.cloud2.x -=0.07;
    this.cloud3.x +=0.06;
    //loop round the side
    if ( this.cloud1.x > this.world.width ) {
      this.cloud1.x = 0 - this.cloud1.width;
    }
    if ( this.cloud2.x < -this.cloud2.width ) {
      this.cloud2.x = this.world.width;
    }
    if ( this.cloud3.x > this.world.width ) {
      this.cloud3.x = 0 - this.cloud3.width;
    }
  }
};
////////////////////////////////////////////////////////////////////
//    Used to update anything in the view/ display messages etc.. //
////////////////////////////////////////////////////////////////////
CitPhaser.update = {
  //changes position of marker and army
  position: function( pos ) {
    //direction is -1 when going right and 1 when going left
    var direction = CitPhaser.position - pos;
    switch ( pos ) {
      case 0:
        //hide Army and display burning Castle (TODO)
        CitPhaser.army.alpha = 0;
        break;
      case 1:
        this.armyPosition( CitPhaser.path1_2, direction );
        break;
      case 2:
        if (direction == -1 ) this.armyPosition( CitPhaser.path1_2, direction );
        else this.armyPosition( CitPhaser.path2_3, direction );
        break;
      case 3:
        if (direction == -1 ) this.armyPosition( CitPhaser.path2_3, direction );
        else this.armyPosition( CitPhaser.path3_4, direction );
        break;
      case 4:
        if (direction == -1 ) this.armyPosition( CitPhaser.path3_4, direction );
        else this.armyPosition( CitPhaser.path4_5, direction );
        break;
      case 5:
        this.armyPosition( CitPhaser.path4_5, direction );
        break;
      case 6:
        //hide Army and display burning Castle (TODO)
        CitPhaser.army.alpha = 0;
        break;
      default:
        //do nothing
        break;
    }
    CitPhaser.positionMarker.frame = pos;
  },
  //
  armyPosition: function( path, direction ) {
    if ( direction == 1 ) {
      for ( var i = path.length - 1; i >=0; --i ) {
        CitPhaser.army.x = path[ i ].x;
        CitPhaser.army.y = path[ i ].y;
      }
    } else {
      for ( var i = 0; i < path.length; ++i ) {
        CitPhaser.army.x = path[ i ].x;
        CitPhaser.army.y = path[ i ].y;
      }
    }
  },
  toggleMoveBoard: function() {
    if ( CitPhaser.moveBoard.y == -485 ) {
      CitPhaser.boardTween.start();
      CitPhaser.boardTweenText.start();
    } else if ( CitPhaser.moveBoard.y == 0 ) {
      CitPhaser.boardTweenTextReverse.start();
      CitPhaser.boardTweenReverse.start();
    }
  },
  bid: function( amount ) {
    //check board is displayed
    if ( CitPhaser.moveBoard.y == 0 ) CitPhaser.moveNumText.setText(amount);
  },
  //display message in speech bubble - lasts 6 secs 
  message: function( text ) {
    if ( !CitPhaser.messageTextTweenFadeOut.isRunning ) {
    CitPhaser.messageText.setText( text );
    CitPhaser.messageTextTweenFadeIn.start();
    CitPhaser.messageBubbleTweenFadeIn.start();
    CitPhaser.messageTextTweenFadeOut.start();
    CitPhaser.messageBubbleTweenFadeOut.start();
    }
  },
  instructions: function() {
    if ( CitPhaser.instructions.alpha == 0 ) {
      //show instructions page 1
      CitPhaser.instructions.alpha = 1;
    } else if ( CitPhaser.instructions.frame == 0 ) {
      //switch to page 2
      CitPhaser.instructions.frame = 1;
    } else if ( CitPhaser.instructions.frame == 1 ) {
      //switch to page 3
      CitPhaser.instructions.frame = 2;
    } else {
      //hide and return to page 1
      CitPhaser.instructions.alpha = 0;
      CitPhaser.instructions.frame = 0;
    }
  },
  // returns if instructions are being shown 
  // should be used to ignore other inputs apart from START
  instructionsShown: function() {
    if ( CitPhaser.instructions.alpha == 1 ) return true;
    return false;
  },
  //updates points totals
  points: function( humPoints, comPoints ) {
    CitPhaser.humPointsText.setText( humPoints );
    CitPhaser.comPointsText.setText( comPoints );
  }
};
