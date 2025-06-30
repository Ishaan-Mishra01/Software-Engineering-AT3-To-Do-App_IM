//score initalisation
let score= 0;

// Ball object and functionality

class Ball {
	constructor(x, y, radius, speedX, speedY) { // inital characteristics: position - (x,y) coords, radius is size and speed is speed in (x,y) direction
		this.x = x; //the 'this' keyword is to reference the current class/object. Here it allows 'x' to be passed as a param/arg
		this.y = y;
		this.radius = radius;
		this.speedX = speedX;
		this.speedY = speedY;
	}
	draw(context) { //this allows the ball to exist. Context is a param that refers to "CanvasRenderingContext2D" which is being passed in which allows the drawing capabilites of canvas to be used
		context.beginPath(); //Begin path is how we start drawin on canvas
		context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);//drawing circle thru the arc method. Last 2 things are start and end angle(in radians).
		context.fillStyle = "red"; // This is the colour
		context.fill(); //this applies the fill style
		context.closePath(); // close the drawing path. Basically 'BEGIN' and 'END' keywords in pseudocode.
	}
	update() { //method to make ball move in canvas. Called within game loop to make the pos of the ball change over time
		this.x += this.speedX; // updates the current pos of the ball in horizontal
		this.y += this.speedY; // same as above but for vertical
	}
}

//Paddle object and functionality

class Paddle {
	constructor(x, y, width, height, speed){ //size is width and height, and speed is only rectilinear, unlike ball.
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.speed = speed;
	}
	draw(context) {
		context.fillStyle = 'orange';
		context.fillRect(this.x, this.y, this.width, this.height); // .fillRect is to create and colour in rectangles

	}
	move(direction) {
		this.x += this.speed * direction;
	}

}

//Brick

class Brick {
	constructor (x, y, width, height){
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.status = 1;
	}
	draw(context){
		if(this.status === 1){
			context.fillStyle = 'green';
			context.fillRect(this.x, this.y, this.width, this.height);
		}
	}
}

const canvas = document.getElementById("canvas"); 
const context = canvas.getContext("2d"); //use get context method to access the "context" of the objects in order to utilise and draw them on the canvas
// param of .getContext() is the context type, which here is 2D as the game is in 2 dimentions.
const ball = new Ball(200, 200, 7, 2, 2); //new instance of the ball to test/see if it works, thru the "new" keyword. 
const paddle = new Paddle(175, canvas.height-10,100,10, 15); //the canvas.height-10 is to place the canvas at the bottom
//const creates an immutable variable


//brick wall

const bricks = [];

function createBrickWall(){
	const brickRowCount = 4;
	const brickColumnCount = 8;
	const brickWidth = 50;
	const brickHeight = 20;
	const brickPadding = 10;

	for (let c = 0; c < brickColumnCount; c++){
		for(let r = 0; r < brickRowCount; r++){
			const x = c * (brickWidth + brickPadding);
			const y = r * (brickHeight + brickPadding);
			bricks.push(new Brick(x, y, brickWidth, brickHeight));
		}
	}
}




// Update and draw bricks

function drawBricks(){
	bricks.forEach(brick =>{
		if(brick.status === 1){
			brick.draw(context);
			//check for collision with ball
			if (ball.x> brick.x && ball.x < brick.x + brick.width &&
				ball.y > brick.y && ball.y < brick.y + brick.height){
					ball.speedY = -ball.speedY;
					brick.status = 0;
					score +=10;
					document.getElementById("score").innerHTML = `Score: ${score}`;
				}
		}
	})
}

//paddle control

document.addEventListener("keydown", (event)=>{
	if(event.key === "ArrowLeft") { //"keydown" event is when key is pressed.
//Additionally, '===' is the JS equivalent of python '==', because in JS, 2 equality signs do not represent a strict equality, rather "they attempt to coerce the value, if they are of different types," To quote Douglas Crockford's excellent JavaScript: The Good Parts.
		paddle.move(-1);
	} else if(event.key === "ArrowRight"){ // 'else if' rather than elif ;-; 
		paddle.move(1);
	}
	//cheat
	else if(event.key === "ArrowDown"){
		paddle.width = canvas.width;
	}
})

document.addEventListener("keyup", (event)=>{
	if(event.key === "ArrowLeft" || event.key === "ArrowRight"){
		paddle.move(0);
	} //cheat
	else if(event.key === "ArrowDown"){
		paddle.width = 100;
	}
})

createBrickWall();

function resetGame(){
	ball.x = 200;
	ball.y = 200;
	ball.speedX = -2;
	ball.speedY = -2;
	paddle.x = 175;
	score = 0;
	bricks.forEach(brick => {
		brick.status =1;
	})
}


function gameLoop(){
	//clear canvas
	context.clearRect(0,0, canvas.clientWidth, canvas.clientHeight);
	
	//draw ball updated position
	ball.update()
	ball.draw(context);
	
	//ball collision detection
	 //sides
	if(ball.x - ball.radius <0 || ball.x + ball.radius > canvas.width){ // '||' is or (the 2 straight lines)
		ball.speedX = -ball.speedX;
	}

	//top side

	if(ball.y - ball.radius < 0) { // similar if statement to the sides, but instead of horizontal, it applies for verticle
		ball.speedY = -ball.speedY;
	}
	
	//paddle collision detection

	if( ball.x + ball.radius > paddle.x && // && is symbol for and
		ball.x - ball.radius < paddle.x + paddle.width &&
		ball.y + ball.radius > paddle.y){
			ball.speedY = -ball.speedY;
		}
	
	//
	if(ball.y + ball.radius > canvas.height){
		alert("Game Over! You Lose!")
		resetGame();
	}

	if(bricks.every(brick => brick.status === 0)){
		alert("Congratulations! You are legend! \n Score: " + score);
		resetGame();
	}
	//paddle
	paddle.draw(context);
	
	//bricks
	drawBricks()

	//loop
	requestAnimationFrame(gameLoop); //built in JS function for smooth animation

}

gameLoop();