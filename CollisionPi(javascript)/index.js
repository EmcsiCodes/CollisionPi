const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const timeSteps = 10000;
const digits = 2;
let countCollisions = 0;

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
    smallBlock = new Block(550,660,100,1,0);
    smallBlockImg = document.getElementById("smallSquare");
    bigBlock = new Block(1100,560,200,Math.pow(100,digits-1),-2/timeSteps);
    bigBlockImg = document.getElementById("bigSquare");
    clack = document.getElementById('clack');
    
}

function background(){
    ctx.fillStyle = 'black';
    ctx.fillRect(0,0,canvas.clientWidth,canvas.height);
    ctx.drawImage(document.getElementById("border"),120,100);
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
            clack.cloneNode().play();
        }
        if(smallBlock.hitBoundary(wall)){
            smallBlock.reverse();
            clack.load();
            clack.cloneNode().play();
        }
        if(bigBlock.hitBoundary(wall + smallBlock.dim)){
        }
        bigBlock.update();
        smallBlock.update();
    }
    smallBlock.show(smallBlockImg, wall);
    bigBlock.show(bigBlockImg, wall + smallBlock.dim);
    //bigBlock.show();
}
function main(){
    //clack.playbackRate = 2;
    preload();
    setInterval(draw,1000/60);
}

main();