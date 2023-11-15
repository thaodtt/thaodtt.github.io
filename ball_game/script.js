var canvas, ctx;
const paddleWidth=100, paddleHeight=10, ballRadius=20, paddleSpeed=20;
const initialBallX=100, initialBallY=100, initialPaddleX=150;
var ballX=initialBallX, ballY=initialBallY, paddleX=initialPaddleX, alive=true;
var angle=random_angle();
var speed=5;

function init() {
  canvas = document.getElementById('myCanvas');
  ctx=canvas.getContext('2d');
  drawPaddle(paddleX, paddleWidth, paddleHeight);
  drawBall(ballX, ballY, ballRadius);
  console.log(angle);
  window.addEventListener("keydown", (evt) =>{
    if (evt.keyCode==37) {
      paddleX = Math.max(0, paddleX - paddleSpeed);
    }
    if (evt.keyCode==39) {
      paddleX = Math.min(canvas.width - paddleWidth, paddleX + paddleSpeed);
    }
  });
//   var button = document.getElementById('startButton');
//   button.style.position = "absolute";
//   button.style.left = canvas.width/2 - 35 +'px';
//   button.style.top = y_pos+'px';
}

function moveBall() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawPaddle(paddleX, paddleWidth, paddleHeight);
  drawBall(ballX, ballY, ballRadius);
  ballX = ballX + speed*Math.cos(angle);
  ballY = ballY - speed*Math.sin(angle);
  if ((ballX - ballRadius < 0) | (ballX + ballRadius > canvas.width)){
    angle = Math.PI - angle;
  }
  if ((ballY - ballRadius < 0)){
    angle = - angle;
  }
  if (ballY + ballRadius > canvas.height){
    if ((ballX > paddleX) & (ballX < paddleX + paddleWidth)){
      angle = - angle;
    }
    else {
      alive = false;
      writeText("You lost!");
    }
  }
  if (alive){
    requestId = requestAnimationFrame(moveBall);  
  }
}

function increaseSpeed(){
  speed = speed + 1;
}

function reduceSpeed(){
  speed = Math.max(1, speed - 1);
}

function random_angle(){
  return Math.PI/4 + (Math.random()-0.5)*0.3;
}

function drawBall(x, y, ballRadius){
  ctx.save();
  ctx.fillStyle= 'red';
  ctx.beginPath();
  ctx.arc(x, y, ballRadius, 0, 2 * Math.PI);
  ctx.fill();
  ctx.restore();
}

function writeText(msg){
  ctx.save();
  ctx.font = "bold 48px serif";
  ctx.fillText(msg, 100, 100);
  ctx.restore();
}

function start() {
  ballX = initialBallX;
  ballY = initialBallY;
  paddleX = initialPaddleX;
  alive=true;
  angle = random_angle();
  requestId = requestAnimationFrame(moveBall);
}
function stop() {
if (requestId) {
    cancelAnimationFrame(requestId);
}
}
function changeSpeed(event) {
  speed = parseInt(event.target.value);
  document.getElementById("speedValue").innerHTML = speed;
  }
function setLevelOne(){
  speed = 5;
}
function setLevelTwo(){
  speed = 10;
}
function setLevelThree(){
  speed = 15;
}

function drawPaddle(paddlePos, paddleWidth, paddleHeight){
    ctx.save();
    ctx.fillStyle= 'black'; // paddle
    ctx.fillRect(paddlePos, canvas.height - paddleHeight, paddleWidth, paddleHeight);
    ctx.restore();
}