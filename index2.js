const canvas = document.getElementById("canvas")
const context = canvas.getContext("2d")

const gridSize = 20
const pacmanRadius = gridSize / 2

let pacmanX = 0
let pacmanY = 0
let direction = "right"

let monsterX = 200
let monsterY = 200

function drawPacman() {
    context.fillStyle = "yellow"
    context.beginPath()
    context.arc(pacmanX, pacmanY, pacmanRadius, 0.2 * Math.PI, 1.8 * Math.PI)
    context.lineTo(pacmanX, pacmanY)
    context.closePath()
    context.fill()
}

function drawMonster() {
    context.fillStyle = "red"
    context.fillRect(monsterX, monsterY, gridSize, gridSize)
}

function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height)
}

function updatePacman() {
    if (direction === "right") {
        pacmanX += gridSize
    } else if (direction === "left") {
        pacmanX -= gridSize
    } else if (direction === "up") {
        pacmanY -= gridSize
    } else if (direction === "down") {
        pacmanY += gridSize
    } 

    if (pacmanX < 0) {
        pacmanX = canvas.width - gridSize
    } else if (pacmanX >= canvas.width) {
        pacmanX = 0
    }

    if (pacmanY < 0) {
        pacmanY = canvas.height - gridSize
    } else if (pacmanY >= canvas.height) {
        pacmanY = 0
    }
}

function updateMonster() {
      const randomDirection = Math.floor(Math.random() * 4)
    if (randomDirection === 0) {
        monsterX += gridSize
    } else if (randomDirection === 1) {
        monsterX -= gridSize
    } else if (randomDirection === 2) {
        monsterY -= gridSize
    } else if (randomDirection === 3) {
        monsterY += gridSize
    }

    if (monsterX < 0) {
        monsterX = canvas.width - gridSize
    } else if (monsterX >= canvas.width) {
        monsterX = 0
    }

    if (monsterY < 0) {
        monsterY = canvas.height - gridSize
    } else if (monsterY >= canvas.height) {
        monsterY = 0
    }
}

function handleKeyDown(event) {
    if (event.key === "ArrowRight") {
        direction = "right"
    } else if (event.key === "ArrowLeft") {
        direction = "left"
    } else if (event.key === "ArrowUp") {
        direction = "up"
    } else if (event.key === "ArrowDown") {
        direction = "down"
    }
}

function checkCollision() {
    if (pacmanX === monsterX && pacmanY === monsterY) {
        alert("Game Over")
        resetGame()
    }
}

function resetGame() {
    pacmanX = 0
    pacmanY = 0
    monsterX = 200
    monsterY = 200
}

function gameLoop() {
    context.clearRect(0, 0, canvas.width, canvas.height)

    clearCanvas();
    updatePacman();
    updateMonster();
    checkCollision();
    drawPacman();
    drawMonster();

}

document.addEventListener("DOMContentLoaded", function() {
    gameLoop();
});
