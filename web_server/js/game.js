// 游戏配置
const config = {
    gridSize: 20,        // 网格大小
    gameSpeed: 150,      // 游戏速度（毫秒）
    canvasSize: 400,     // 画布大小
    initialLength: 3     // 初始蛇长度
};

// 游戏状态
let snake = [];          // 蛇的身体
let food = null;         // 食物位置
let direction = 'right'; // 移动方向
let nextDirection = 'right';
let score = 0;           // 分数
let gameLoop = null;     // 游戏循环
let isPaused = false;    // 暂停状态
let isGameOver = true;   // 游戏结束状态

// 获取画布和上下文
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const statusElement = document.getElementById('gameStatus');

// 初始化游戏
function initGame() {
    // 初始化蛇
    const center = Math.floor(config.canvasSize / config.gridSize / 2);
    snake = [];
    for (let i = 0; i < config.initialLength; i++) {
        snake.push({ x: center - i, y: center });
    }

    // 生成第一个食物
    generateFood();

    // 重置游戏状态
    direction = 'right';
    nextDirection = 'right';
    score = 0;
    isGameOver = false;
    isPaused = false;
    updateScore();
    statusElement.textContent = '游戏开始！';
}

// 生成食物
function generateFood() {
    while (true) {
        food = {
            x: Math.floor(Math.random() * (config.canvasSize / config.gridSize)),
            y: Math.floor(Math.random() * (config.canvasSize / config.gridSize))
        };
        // 确保食物不会生成在蛇身上
        if (!snake.some(segment => segment.x === food.x && segment.y === food.y)) {
            break;
        }
    }
}

// 更新分数
function updateScore() {
    scoreElement.textContent = `分数: ${score}`;
}

// 游戏主循环
function gameUpdate() {
    if (isPaused || isGameOver) return;

    // 更新方向
    direction = nextDirection;

    // 获取蛇头
    const head = { ...snake[0] };

    // 根据方向移动蛇头
    switch (direction) {
        case 'up': head.y--; break;
        case 'down': head.y++; break;
        case 'left': head.x--; break;
        case 'right': head.x++; break;
    }

    // 检查是否撞墙
    if (head.x < 0 || head.x >= config.canvasSize / config.gridSize ||
        head.y < 0 || head.y >= config.canvasSize / config.gridSize) {
        gameOver();
        return;
    }

    // 检查是否撞到自己
    if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        gameOver();
        return;
    }

    // 移动蛇
    snake.unshift(head);

    // 检查是否吃到食物
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        updateScore();
        generateFood();
    } else {
        snake.pop();
    }

    // 绘制游戏
    drawGame();
}

// 绘制游戏
function drawGame() {
    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 绘制网格
    ctx.strokeStyle = '#eee';
    for (let i = 0; i < config.canvasSize; i += config.gridSize) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, config.canvasSize);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(config.canvasSize, i);
        ctx.stroke();
    }

    // 绘制蛇
    snake.forEach((segment, index) => {
        ctx.fillStyle = index === 0 ? '#ff0000' : '#00ff00';
        ctx.fillRect(
            segment.x * config.gridSize,
            segment.y * config.gridSize,
            config.gridSize - 1,
            config.gridSize - 1
        );
    });

    // 绘制食物
    ctx.fillStyle = '#ff0';
    ctx.fillRect(
        food.x * config.gridSize,
        food.y * config.gridSize,
        config.gridSize - 1,
        config.gridSize - 1
    );
}

// 游戏结束
function gameOver() {
    isGameOver = true;
    clearInterval(gameLoop);
    statusElement.textContent = '游戏结束！按空格键重新开始';
}

// 开始游戏
function startGame() {
    if (isGameOver) {
        initGame();
        gameLoop = setInterval(gameUpdate, config.gameSpeed);
    } else if (isPaused) {
        isPaused = false;
        statusElement.textContent = '游戏继续';
    }
}

// 暂停游戏
function pauseGame() {
    if (!isGameOver) {
        isPaused = !isPaused;
        statusElement.textContent = isPaused ? '游戏暂停' : '游戏继续';
    }
}

// 键盘控制
document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'ArrowUp':
            if (direction !== 'down') nextDirection = 'up';
            break;
        case 'ArrowDown':
            if (direction !== 'up') nextDirection = 'down';
            break;
        case 'ArrowLeft':
            if (direction !== 'right') nextDirection = 'left';
            break;
        case 'ArrowRight':
            if (direction !== 'left') nextDirection = 'right';
            break;
        case ' ':
            if (isGameOver) {
                startGame();
            } else {
                pauseGame();
            }
            break;
    }
});

// 初始化游戏界面
drawGame(); 