const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let timeSteps = 10;
let digits = 1;
let countCollisions = 0;
let gameStopped = false;
let gameResseted = false;

class Block{
    constructor(x,y,dim,m,v){
        this.x = x;
        this.tx = x;
        this.y = y;
        this.dim = dim;
        this.m = m;
        this.v = v;
    }

    collide(other){
        return (this.x + this.dim > other.x);
    }

    hitBoundary(x){
        return (this.x <= x);
    }

    reverse(){
        this.v = -this.v;
    } 
    
    bounce(other){
        let sumM = this.m + other.m;
        let newV = (this.m - other.m)/sumM * this.v + 2 * other.m / sumM * other.v;
        return newV;
    }

    update(){
        this.x += this.v;
    }

    show(blockImg,dis){
        if(this.x<=dis) this.tx = dis;
        else this.tx = this.x;
        ctx.drawImage(blockImg,this.tx,this.y,this.dim,this.dim);
    }
}

let smallBlockImg;
let bigBlockImg;
let smallBlock;
let bigBlock;
let clack;
const wall = 160;


function preload(){
    timeSteps = 100000;
    smallBlock = new Block(550,460,100,1,0);
    smallBlockImg = document.getElementById("smallSquare");
    bigBlock = new Block(1100,360,200,Math.pow(100,digits-1),-2/timeSteps);
    bigBlockImg = document.getElementById("bigSquare");
    clack = document.getElementById('clack');
    countCollisions = 0;
    // restartButton = new Button(100,100,200,200,document.getElementById('restartButton'));
    // restartButton.create();
}

function background(){
    ctx.fillStyle = 'black';
    ctx.fillRect(0,0,canvas.clientWidth,canvas.height);
    ctx.drawImage(document.getElementById("border"),120,60);
    ctx.drawImage(document.getElementById("borderdown"),160, canvas.height - 140);
    ctx.drawImage(document.getElementById("borderdown"),700, canvas.height - 140);
    ctx.drawImage(document.getElementById("borderdown"),1100, canvas.height - 140);
    ctx.drawImage(document.getElementById("pi"),280,590,80,80);
    ctx.fillStyle = 'white';
    ctx.font = "48px Consolas";
    let str = countCollisions.toString();
    str = "# Collisions:  " + str;
    let strlength = ctx.measureText(str).width;
    ctx.fillText(str, canvas.clientWidth/2 - strlength/2, 75);
    str = "Set # of    's digits: ";
    ctx.fillText(str,50,650);
    str = "1" + "0".repeat(2*(digits - 1)%3) + ",000".repeat(2*(digits - 1)/3) + " kg";
    strlength = ctx.measureText(str).width;
    ctx.fillText(str,bigBlock.x + bigBlock.dim / 2 - strlength/2,bigBlock.y - 20);
    str = "1 kg";
    strlength = ctx.measureText(str).width;
    ctx.fillText(str,smallBlock.x + smallBlock.dim/2 - strlength/2,smallBlock.y - 20);
}

function draw(){
    background();
    for(let i = 1; i<timeSteps; i++){
        if(smallBlock.collide(bigBlock)){
            v1 = smallBlock.bounce(bigBlock);
            v2 = bigBlock.bounce(smallBlock);
            smallBlock.v = v1;
            bigBlock.v = v2;
            smallBlock.tx = bigBlock.x;
           //clack.cloneNode().play();
            countCollisions++;
        }
        if(smallBlock.hitBoundary(wall)){
            smallBlock.reverse();
            //clack.cloneNode().play();
            countCollisions++;
            console.log()
        }
        if(bigBlock.hitBoundary(wall + smallBlock.dim)){
        }
        bigBlock.update();
        smallBlock.update();
    }
    smallBlock.show(smallBlockImg, wall);
    bigBlock.show(bigBlockImg, wall + smallBlock.dim);
    console.log(countCollisions);
    //bigBlock.show();
}

function pause(){
    if(gameStopped == false) {
        gameStopped = true;
        document.getElementById("pauseButton").src="data/startButton.png";
    }
    else {
        gameStopped = false;
        document.getElementById("pauseButton").src="data/stopButton.png"
    }
}

function reset(){
    digits = document.getElementById("piNum").value;
    if(digits<1) digits = 1;
    if(digits < 5) timeSteps = 10;
    if(digits >= 6 && digits <= 7) timeSteps = 10000;
    if(digits >= 8) timeSteps = 300000;
    preload();
    draw();
    gameStopped = false;
    pause();
}

function main(){
    if(digits<1) digits = 1;
    preload();
    setInterval(function(){
        if(gameStopped == false) draw();
    },1000/60);
}

main();