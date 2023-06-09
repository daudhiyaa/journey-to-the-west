const canvas = document.querySelector("canvas");
const cost = document.getElementById("cost");
const canvasContext = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// VARIABLES

let path = [];
let solutions = [];
let start, end;

let tc = 1;
let boundaries = [];
let pellets = [];
let map = [];

const keys = {
  w: {
    pressed: false,
  },
  a: {
    pressed: false,
  },
  s: {
    pressed: false,
  },
  d: {
    pressed: false,
  },
};
let lastKey = "";

// CLASSES

class Boundary {
  static width = 40;
  static height = 40;

  constructor({ position }) {
    this.position = position;
    this.width = 40;
    this.height = 40;
    this.color = "blue";
  }

  draw() {
    canvasContext.fillStyle = this.color;
    canvasContext.fillRect(
      this.position.x,
      this.position.y,
      this.width,
      this.height
    );
  }
}

class Player {
  constructor({ position, velocity }) {
    this.position = position;
    this.velocity = velocity;
    this.radius = 15;
    this.color = "yellow";
  }

  draw() {
    canvasContext.beginPath();
    canvasContext.arc(
      this.position.x,
      this.position.y,
      this.radius,
      0,
      Math.PI * 2
    );
    canvasContext.fillStyle = this.color;
    canvasContext.fill();
    canvasContext.closePath();
  }

  update() {
    this.draw();
    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
  }
}

class Pellet {
  constructor({ position }) {
    this.position = position;
    this.radius = 3;
    this.color = "white";
  }

  draw() {
    canvasContext.beginPath();
    canvasContext.arc(
      this.position.x,
      this.position.y,
      this.radius,
      0,
      Math.PI * 2
    );
    canvasContext.fillStyle = this.color;
    canvasContext.fill();
    canvasContext.closePath();
  }
}

class Ghost {
  // static speed = 2;
  constructor({ position, velocity, color = "red" }) {
    this.position = position;
    this.velocity = velocity;
    this.radius = 15;
    this.color = color;
    this.prevCollisions = [];
    // this.speed = 0;
    this.scared = false;
  }

  draw() {
    canvasContext.beginPath();
    canvasContext.arc(
      this.position.x,
      this.position.y,
      this.radius,
      0,
      Math.PI * 2
    );
    canvasContext.fillStyle = this.scared ? "blue" : this.color;
    canvasContext.fill();
    canvasContext.closePath();
  }

  update() {
    this.draw();
    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
  }
}

class Cell {
  constructor(x, y, dist, prev) {
    this.x = x;
    this.y = y;
    this.dist = dist; // distance
    this.prev = prev; // parent cell in the path
  }
  toString() {
    return "(" + this.x + ", " + this.y + ")";
  }
}

class Maze {
  shortestPath(labyrint, start, end) {
    const sx = start[0];
    const sy = start[1];
    const dx = end[0];
    const dy = end[1];

    if (labyrint[sx][sy] != "." || labyrint[dx][dy] != ".") {
      console.log("start or end point is invalid.");
      return;
    }

    // initialize the cells
    const row = labyrint.length;
    const col = labyrint[0].length;

    const cells = [];
    for (let i = 0; i < row; i++) {
      cells[i] = [];
      for (let j = 0; j < col; j++) {
        if (labyrint[i][j] === ".") {
          cells[i][j] = new Cell(i, j, Number.MAX_VALUE, null);
        }
      }
    }

    // BFS
    let queue = [],
      dest = null,
      p;
    const src = cells[sx][sy];

    src.dist = 0;
    queue.push(src);
    while ((p = queue.shift()) != null) {
      // find destination
      if (p.x == dx && p.y == dy) {
        dest = p;
        break;
      }

      this.visit(cells, queue, p.x - 1, p.y, p, row, col);
      this.visit(cells, queue, p.x, p.y - 1, p, row, col);
      this.visit(cells, queue, p.x + 1, p.y, p, row, col);
      this.visit(cells, queue, p.x, p.y + 1, p, row, col);
    }

    // compose the path if path exists
    if (dest == null) {
      console.log("dest is null. there is no path.");
      return;
    } else {
      p = dest;
      do {
        path.unshift(p);
      } while ((p = p.prev) != null);

      path.forEach((now) => {
        let tmp = [];
        tmp.push(now.x, now.y);
        solutions.push(tmp);
      });
      cost.innerHTML = path.length;

      solutions.forEach((solution) => {
        console.log(solution);
      });
    }
  }

  // function to update cell visiting status, Time O(1), Space O(1)
  visit(cells, queue, x, y, parent, row, col) {
    if (x < 0 || x >= row || y < 0 || y >= col || cells[x][y] == null) return;

    const dist = parent.dist + 1;
    const p = cells[x][y];

    if (dist < p.dist) {
      p.dist = dist;
      p.prev = parent;
      queue.push(p);
    }
  }
}

// STARTING PROGRAM

function mulai() {
  // reset variable values
  path = [];
  solutions = [];

  boundaries = [];
  pellets = [];
  map = [];

  function generateMaze() {
    const lst = [".", "#", ".", ".", "."];
    const row = Math.floor(Math.random() * 31) + 10;
    const col = Math.floor(Math.random() * 31) + 10;

    for (let i = 0; i < row; i++) {
      const tmp = [];
      for (let j = 0; j < col; j++) {
        tmp.push(lst[Math.floor(Math.random() * lst.length)]);
      }
      map.push(tmp);
    }
  }

  generateMaze();

  const maze = new Maze();

  for (let i = 1; i <= tc; i++) {
    start = [1, 1];
    end = [10, 9];
    console.log(`CASE ${i}: `);
    maze.shortestPath(map, start, end);
  }

  map.forEach((row, i) => {
    row.forEach((symbol, j) => {
      switch (symbol) {
        case "#":
          boundaries.push(
            new Boundary({
              position: { x: Boundary.width * j, y: Boundary.height * i },
            })
          );
          break;
      }
    });
  });

  const player = new Player({
    position: {
      x: Boundary.width + Boundary.width / 2,
      y: Boundary.height + Boundary.height / 2,
    },
    velocity: { x: 0, y: 0 },
  });

  const ghosts = [
    new Ghost({
      position: {
        x:
          Boundary.width * Math.floor(Math.random() * (map[0].length - 4) + 2) +
          Boundary.width / 2,
        y: Boundary.height + Boundary.height / 2,
      },
      velocity: {
        x: 0,
        y: 0,
      },
    }),
    new Ghost({
      position: {
        x: Boundary.width * 6 + Boundary.width / 2,
        y: Boundary.height * 4 + Boundary.height / 2,
      },
      velocity: {
        x: 0,
        y: 0,
      },
      color: "pink",
    }),
  ];

  for (let i = solutions.length - 1; i >= 0; i--) {
    const solution = solutions[i];
    pellets.push(
      new Pellet({
        position: {
          x: Boundary.width * solution[1] + Boundary.width / 2,
          y: Boundary.height * solution[0] + Boundary.height / 2,
        },
      })
    );
  }

  function animate() {
    requestAnimationFrame(animate);
    canvasContext.clearRect(0, 0, canvas.width, canvas.height);

    boundaries.forEach((boundary) => {
      boundary.draw();
    });

    for (let i = 0; i < pellets.length; i++) {
      const pellet = pellets[i];
      // console.log(pellet.position.x);
      pellet.draw();
    }
    player.update();

    // buat harus pressed
    player.velocity.y = 0;
    player.velocity.x = 0;

    ghosts.forEach((ghost) => {
      ghost.update();
    });
  }

  let cnt = 0;
  let i = 0;

  addEventListener("keydown", ({ key }) => {
    const xNow = solutions[cnt + 1][0] - solutions[cnt][0];
    const yNow = solutions[cnt + 1][1] - solutions[cnt][1];

    if (key === "w") {
      i++;
      console.log(`tes ${i}`);
      player.velocity.y = -40;
    } else if (key === "a") player.velocity.x = -40;
    else if (key === "s") player.velocity.y = 40;
    else if (key === "d") player.velocity.x = 40;
    else if (key === "e") {
      console.log(xNow, yNow);
      if (xNow < 0) player.velocity.y = -40;
      else if (xNow > 0) player.velocity.y = 40;
      else if (yNow < 0) player.velocity.x = -40;
      else if (yNow > 0) player.velocity.x = 40;
      cnt++;
      // solutions.shift();
    }
  });

  animate();
}
