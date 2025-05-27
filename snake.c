#include <ncurses.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>

// 游戏区域大小
#define HEIGHT 20
#define WIDTH 40

// 方向键
#define UP_KEY     KEY_UP
#define DOWN_KEY   KEY_DOWN
#define LEFT_KEY   KEY_LEFT
#define RIGHT_KEY  KEY_RIGHT

// 游戏状态
typedef struct {
    int x, y;    // 坐标
} Position;

// 蛇的结构
typedef struct {
    Position pos[100];  // 蛇身坐标数组
    int length;         // 当前长度
    int direction;      // 移动方向
} Snake;

// 食物结构
typedef struct {
    Position pos;       // 食物位置
} Food;

// 游戏状态
typedef struct {
    Snake snake;
    Food food;
    int score;
    bool running;
} Game;

// 初始化游戏
void init_game(Game* game) {
    // 初始化随机数
    srand(time(NULL));
    
    // 初始化蛇
    game->snake.length = 3;
    game->snake.direction = RIGHT_KEY;
    game->snake.pos[0].x = WIDTH/2;
    game->snake.pos[0].y = HEIGHT/2;
    game->snake.pos[1].x = WIDTH/2-1;
    game->snake.pos[1].y = HEIGHT/2;
    game->snake.pos[2].x = WIDTH/2-2;
    game->snake.pos[2].y = HEIGHT/2;
    
    // 初始化食物
    game->food.pos.x = rand() % (WIDTH-2) + 1;
    game->food.pos.y = rand() % (HEIGHT-2) + 1;
    
    // 初始化分数
    game->score = 0;
    game->running = true;
}

// 生成新的食物
void new_food(Game* game) {
    bool valid;
    do {
        valid = true;
        game->food.pos.x = rand() % (WIDTH-2) + 1;
        game->food.pos.y = rand() % (HEIGHT-2) + 1;
        
        // 确保食物不会出现在蛇身上
        for(int i = 0; i < game->snake.length; i++) {
            if(game->food.pos.x == game->snake.pos[i].x && 
               game->food.pos.y == game->snake.pos[i].y) {
                valid = false;
                break;
            }
        }
    } while(!valid);
}

// 绘制游戏界面
void draw(Game* game) {
    // 清屏
    clear();
    
    // 绘制边框
    for(int i = 0; i < HEIGHT; i++) {
        mvaddch(i, 0, '|');
        mvaddch(i, WIDTH-1, '|');
    }
    for(int i = 0; i < WIDTH; i++) {
        mvaddch(0, i, '-');
        mvaddch(HEIGHT-1, i, '-');
    }
    
    // 绘制蛇
    for(int i = 0; i < game->snake.length; i++) {
        if(i == 0) {
            // 蛇头
            attron(COLOR_PAIR(1));
            mvaddch(game->snake.pos[i].y, game->snake.pos[i].x, '@');
            attroff(COLOR_PAIR(1));
        } else {
            // 蛇身
            attron(COLOR_PAIR(2));
            mvaddch(game->snake.pos[i].y, game->snake.pos[i].x, 'o');
            attroff(COLOR_PAIR(2));
        }
    }
    
    // 绘制食物
    attron(COLOR_PAIR(3));
    mvaddch(game->food.pos.y, game->food.pos.x, '*');
    attroff(COLOR_PAIR(3));
    
    // 显示分数
    mvprintw(0, WIDTH/2-5, "Score: %d", game->score);
    
    // 刷新屏幕
    refresh();
}

// 移动蛇
void move_snake(Game* game) {
    // 保存蛇头位置
    Position new_head = game->snake.pos[0];
    
    // 根据方向移动蛇头
    switch(game->snake.direction) {
        case UP_KEY:
            new_head.y--;
            break;
        case DOWN_KEY:
            new_head.y++;
            break;
        case LEFT_KEY:
            new_head.x--;
            break;
        case RIGHT_KEY:
            new_head.x++;
            break;
    }
    
    // 检查是否撞墙
    if(new_head.x <= 0 || new_head.x >= WIDTH-1 ||
       new_head.y <= 0 || new_head.y >= HEIGHT-1) {
        game->running = false;
        return;
    }
    
    // 检查是否撞到自己
    for(int i = 0; i < game->snake.length; i++) {
        if(new_head.x == game->snake.pos[i].x && 
           new_head.y == game->snake.pos[i].y) {
            game->running = false;
            return;
        }
    }
    
    // 移动蛇身
    for(int i = game->snake.length-1; i > 0; i--) {
        game->snake.pos[i] = game->snake.pos[i-1];
    }
    game->snake.pos[0] = new_head;
    
    // 检查是否吃到食物
    if(new_head.x == game->food.pos.x && new_head.y == game->food.pos.y) {
        game->score++;
        game->snake.length++;
        new_food(game);
    }
}

int main() {
    // 初始化ncurses
    initscr();
    noecho();
    curs_set(0);
    keypad(stdscr, TRUE);
    timeout(100);
    
    // 初始化颜色
    start_color();
    init_pair(1, COLOR_RED, COLOR_BLACK);    // 蛇头
    init_pair(2, COLOR_GREEN, COLOR_BLACK);  // 蛇身
    init_pair(3, COLOR_YELLOW, COLOR_BLACK); // 食物
    
    // 初始化游戏
    Game game;
    init_game(&game);
    
    // 主游戏循环
    while(game.running) {
        // 处理输入
        int key = getch();
        switch(key) {
            case UP_KEY:
                if(game.snake.direction != DOWN_KEY)
                    game.snake.direction = UP_KEY;
                break;
            case DOWN_KEY:
                if(game.snake.direction != UP_KEY)
                    game.snake.direction = DOWN_KEY;
                break;
            case LEFT_KEY:
                if(game.snake.direction != RIGHT_KEY)
                    game.snake.direction = LEFT_KEY;
                break;
            case RIGHT_KEY:
                if(game.snake.direction != LEFT_KEY)
                    game.snake.direction = RIGHT_KEY;
                break;
            case 'q':
                game.running = false;
                break;
        }
        
        // 移动蛇
        move_snake(&game);
        
        // 绘制游戏
        draw(&game);
        
        // 控制游戏速度
        usleep(100000);  // 100ms
    }
    
    // 游戏结束
    mvprintw(HEIGHT/2, WIDTH/2-10, "Game Over! Score: %d", game.score);
    mvprintw(HEIGHT/2+1, WIDTH/2-15, "Press any key to exit...");
    refresh();
    getch();
    
    // 清理
    endwin();
    return 0;
} 