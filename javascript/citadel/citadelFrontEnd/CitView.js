var Cit = {};
//holds all the view items and creates moving background
Cit.View = function (game) {

	this.cloud1 = null;
	this.cloud2 = null;
	this.cloud3 = null;	

	Cit.positionMarker = null;
	Cit.p1Castle = null;
	Cit.p2Castle = null;
	Cit.p1Tower = null;
	Cit.p2Tower = null;
	Cit.army = null;
	//points of the army positions;
	Cit.point1_2 = {
	    'x': [ 137, 564 ],
	    'y': [ 552, 760 ]
		};
	Cit.point2_3 = {
	    'x': [ 564, 994 ],
	    'y': [ 760, 767 ]
		};
	Cit.point3_4 = {
	    'x': [ 994, 1476 ],
	    'y': [ 767, 705 ]
		};
	Cit.point4_5 = {
	    'x': [ 1476, 1760 ],
	    'y': [ 705, 565 ]
		};

	Cit.path1_2 = [];
	Cit.path2_3 = [];
	Cit.path3_4 = [];
	Cit.path4_5 = [];

	Cit.boardTween = null;
	Cit.boardTweenText = null;
	Cit.messageBubbleTweenFadeIn = null;
	Cit.messageTextTweenFadeIn = null;
	Cit.messageBubbleTweenFadeOut = null;
	Cit.messageTextTweenFadeOut = null;

	Cit.humPointsText = null;
	Cit.comPointsText = null;
	Cit.moveNumText = null;
	Cit.messageText = null;
	Cit.moveBoard = null;

	Cit.position = 3;
};
Cit.View.prototype = {

	preload: function() {

	    this.load.image('bg', 'assets/bg.png');
	    this.load.spritesheet('positionMarker', 'assets/posInfo.png',841,65);
	    this.load.spritesheet('castle', 'assets/castles.png',227,288);
	    this.load.spritesheet('tower', 'assets/towers.png',80,142, 2);
	    this.load.spritesheet('instructions', 'assets/instructions.png',1920,1080);
	    this.load.image('cloud1', 'assets/cloud1.png');            
	    this.load.image('cloud2', 'assets/cloud2.png');            
	    this.load.image('cloud3', 'assets/cloud3.png'); 
	    this.load.image('comTotal', 'assets/comTotal.png');
	    this.load.image('humTotal', 'assets/humTotal.png');
			this.load.image('messageBubble', 'assets/messageBubble.png');
			this.load.image('moveBoard', 'assets/moveBoard.png');
	    this.load.image('army', 'assets/army.png');           
	},
	create: function() {

	    var bg = this.add.sprite(0, 0, 'bg');
    	this.cloud1 = this.add.sprite(640,358, 'cloud1');
	    this.cloud2 = this.add.sprite(1436,189, 'cloud2');
	    this.cloud3 = this.add.sprite(114,-15, 'cloud3');

	    var humTotal = this.add.sprite(20, 20, 'humTotal');
	    var comTotal = this.add.sprite(1781, 20, 'comTotal');

	    Cit.positionMarker = this.add.sprite(595,991, 'positionMarker');
	    Cit.positionMarker.frame = 3;

	    Cit.p1Castle = this.add.sprite(0,264, 'castle');
	    Cit.p1Castle.frame = 1;

	    Cit.p2Castle = this.add.sprite(1669,287, 'castle');

	    Cit.p1Tower = this.add.sprite(524,593, 'tower');
	    Cit.p1Tower.frame = 1;

	    Cit.p2Tower = this.add.sprite(1440,569, 'tower');

	    Cit.army = this.add.sprite(994,767, 'army');
	    Cit.army.anchor.set(0.5);


	    //setup move board above screen
	    Cit.moveBoard = this.add.sprite(727,-485, 'moveBoard');
			var moveStyle = { font: "65px Arial", fill: "#ffffff", align: "center" };
			Cit.moveNumText = this.add.text(965, -187, "1", moveStyle);
			//tween the board down
			Cit.boardTween = this.add.tween(Cit.moveBoard).to({ y: '+485' }, 500,Phaser.Easing.Linear.None, false);
			Cit.boardTweenText = this.add.tween(Cit.moveNumText).to({ y: '+485' }, 500,Phaser.Easing.Linear.None, false);
			//reverse the board
			Cit.boardTweenReverse = this.add.tween(Cit.moveBoard).to({ y: '-485' }, 500,Phaser.Easing.Linear.None, false);
			Cit.boardTweenTextReverse = this.add.tween(Cit.moveNumText).to({ y: '-485' }, 500,Phaser.Easing.Linear.None, false);

			//setup message text and bubble
			var messageBubble = this.add.sprite(315,-1, 'messageBubble');
			var messageStyle = { font: "25px Arial", fill: "#000000", align: "left" };
			Cit.messageText = this.add.text(373, 74, "", messageStyle);
			messageBubble.alpha = 0;
			Cit.messageText.alpha = 0;
			//fade in tweens
			Cit.messageBubbleTweenFadeIn = this.add.tween(messageBubble).to({alpha: 1}, 500,Phaser.Easing.Linear.None, false);
			Cit.messageTextTweenFadeIn = this.add.tween(Cit.messageText).to({alpha: 1}, 500,Phaser.Easing.Linear.None, false);
			//fade out  tweens - delay (6500 - 500) is how long the message will stay for
			Cit.messageBubbleTweenFadeOut = this.add.tween(messageBubble).to({alpha: 0}, 500,Phaser.Easing.Linear.None, false, 6500);
			Cit.messageTextTweenFadeOut = this.add.tween(Cit.messageText).to({alpha: 0}, 500,Phaser.Easing.Linear.None, false, 6500);

			//add point totals
			var totalStyle = { font: "45px Arial", fill: "#ffffff", align: "center" };
			Cit.humPointsText = this.add.text(55, 73, "50", totalStyle);
			Cit.comPointsText = this.add.text(1815, 73,"50", totalStyle);

			// display instructions
			Cit.instructions = this.add.sprite(0,0, 'instructions');

	   this.plot();

	},
	//plots the path of the army between the points (x4)
	plot: function () {
	    var x = 1 / this.game.width;

	    for (var i = 0; i <= 1; i += x)
	    {
	        
	      var px = this.math.catmullRomInterpolation(Cit.point1_2.x, i);
	      var py = this.math.catmullRomInterpolation(Cit.point1_2.y, i);
	      Cit.path1_2.push( { x: px, y: py });
	    }
	    for (var i = 0; i <= 1; i += x)
	    {
	        
	      var px = this.math.catmullRomInterpolation(Cit.point2_3.x, i);
	      var py = this.math.catmullRomInterpolation(Cit.point2_3.y, i);
	      Cit.path2_3.push( { x: px, y: py });
	    }
	    for (var i = 0; i <= 1; i += x)
	    {
	        
	      var px = this.math.catmullRomInterpolation(Cit.point3_4.x, i);
	      var py = this.math.catmullRomInterpolation(Cit.point3_4.y, i);
	      Cit.path3_4.push( { x: px, y: py });
	    }
	    for (var i = 0; i <= 1; i += x)
	    {
	        
	      var px = this.math.catmullRomInterpolation(Cit.point4_5.x, i);
	      var py = this.math.catmullRomInterpolation(Cit.point4_5.y, i);
	      Cit.path4_5.push( { x: px, y: py });
	    }

	},
	update: function () {

		//animated clouds!
		//varied speeds and direction
		this.cloud1.x +=0.05;
		this.cloud2.x -=0.07;
		this.cloud3.x +=0.06;
		//loop round the side
	  if (this.cloud1.x > this.world.width)
	  {
	      this.cloud1.x = 0 - this.cloud1.width;
	  }
	  if (this.cloud2.x < -this.cloud2.width)
	  {
	      this.cloud2.x = this.world.width;
	  }
	  if (this.cloud3.x > this.world.width)
	  {
	      this.cloud3.x = 0 - this.cloud3.width;
	  }
	 
	}
};
////////////////////////////////////////////////////////////////////
//    Used to update anything in the view/ display messages etc.. //
////////////////////////////////////////////////////////////////////
Cit.update = {
	//changes position of marker and army
	position: function(pos) {
		//direction is -1 when going right and 1 when going left
		var direction = Cit.position - pos;
		switch(pos) {

			case 0:
				//hide Army and display burning Castle (TODO)
				Cit.army.alpha = 0;
				break;
			case 1:
				this.armyPosition(Cit.path1_2, direction);
				break;
			case 2:
				if (direction == -1) this.armyPosition(Cit.path1_2, direction);
				else this.armyPosition(Cit.path2_3, direction);
				break;
			case 3:
				if (direction == -1) this.armyPosition(Cit.path2_3, direction);
				else this.armyPosition(Cit.path3_4, direction);
				break;
			case 4:
				if (direction == -1) this.armyPosition(Cit.path3_4, direction);
				else this.armyPosition(Cit.path4_5, direction);
				break;
			case 5:
				this.armyPosition(Cit.path4_5, direction);
				break;
			case 6:
				//hide Army and display burning Castle (TODO)
				Cit.army.alpha = 0;
				break;
			default:
				//do nothing
				break;
		}
		Cit.positionMarker.frame = pos;
	},
	//
	armyPosition: function(path, direction) {
		if(direction == 1)
		{
			for(var i = path.length - 1; i >=0; --i)
			{
				Cit.army.x = path[i].x;
	  		Cit.army.y = path[i].y;
			}
		}
		else {
			for(var i = 0; i < path.length; ++i)
			{
				Cit.army.x = path[i].x;
	  		Cit.army.y = path[i].y;
			}
		}
	},
	toggleMoveBoard: function() {

		if(Cit.moveBoard.y == -485) {
			Cit.boardTween.start();
			Cit.boardTweenText.start();

		}
		else if(Cit.moveBoard.y == 0) {
			Cit.boardTweenTextReverse.start();
			Cit.boardTweenReverse.start();
		}
	},
	bid: function(amount) {
		//check board is displayed
		if (Cit.moveBoard.y == 0) Cit.moveNumText.setText(amount);
	},
	//display message in speech bubble - lasts 6 secs 
	message: function(text) {
		if(!Cit.messageTextTweenFadeOut.isRunning) {
		Cit.messageText.setText(text);
		Cit.messageTextTweenFadeIn.start();
		Cit.messageBubbleTweenFadeIn.start();
		Cit.messageTextTweenFadeOut.start();
		Cit.messageBubbleTweenFadeOut.start();
		}
		
	},
	instructions: function() {
		//show instructions page 1
		if(Cit.instructions.alpha == 0) {
			Cit.instructions.alpha = 1;
		}
		//switch to page 2
		else if(Cit.instructions.frame == 0) {
			Cit.instructions.frame = 1;
		}
		//switch to page 3
		else if(Cit.instructions.frame == 1) {
			Cit.instructions.frame = 2;
		}
		//hide and return to page 1
		else {
			Cit.instructions.alpha = 0;
			Cit.instructions.frame = 0;
		}
	},
	// returns if instructions are being shown 
	// should be used to ignore other inputs apart from START
	instructionsShown: function() {
		if(Cit.instructions.alpha == 1) return true;
		return false;
	}
};