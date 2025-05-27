#!/usr/bin/env python3
import curses
import random
import time

# 游戏设置
HEIGHT = 20
WIDTH = 40
SPEED = 0.1  # 游戏速度（秒）

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height = HEIGHT
        self.width = WIDTH
        
        # 初始化颜色
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)     # 蛇头
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # 蛇身
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # 食物
        
        # 初始化游戏窗口
        self.win = curses.newwin(self.height + 2, self.width + 2, 0, 0)
        self.win.keypad(1)
        self.win.timeout(100)
        
        # 初始化游戏状态
        self.reset_game()
    
    def reset_game(self):
        """重置游戏状态"""
        # 初始化蛇的位置（从中间开始）
        self.snake = [
            [self.height//2, self.width//2],      # 蛇头
            [self.height//2, self.width//2 - 1],  # 蛇身
            [self.height//2, self.width//2 - 2]   # 蛇尾
        ]
        self.direction = curses.KEY_RIGHT
        self.score = 0
        self.food = self.generate_food()
        self.game_over = False
    
    def generate_food(self):
        """生成新的食物"""
        while True:
            food = [
                random.randint(1, self.height-2),
                random.randint(1, self.width-2)
            ]
            if food not in self.snake:
                return food
    
    def draw(self):
        """绘制游戏界面"""
        # 清空窗口
        self.win.clear()
        
        # 绘制边框
        self.win.border(0)
        
        # 绘制蛇
        for i, (y, x) in enumerate(self.snake):
            if i == 0:  # 蛇头
                self.win.addstr(y, x, '@', curses.color_pair(1))
            else:       # 蛇身
                self.win.addstr(y, x, 'o', curses.color_pair(2))
        
        # 绘制食物
        self.win.addstr(self.food[0], self.food[1], '*', curses.color_pair(3))
        
        # 显示分数
        score_text = f"Score: {self.score}"
        self.win.addstr(0, (self.width - len(score_text))//2, 
                       score_text, curses.color_pair(3))
        
        # 刷新窗口
        self.win.refresh()
    
    def move(self):
        """移动蛇"""
        # 获取蛇头位置
        head = self.snake[0].copy()
        
        # 根据方向移动蛇头
        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1
        
        # 检查是否撞墙
        if (head[0] <= 0 or head[0] >= self.height-1 or
            head[1] <= 0 or head[1] >= self.width-1):
            self.game_over = True
            return
        
        # 检查是否撞到自己
        if head in self.snake:
            self.game_over = True
            return
        
        # 移动蛇
        self.snake.insert(0, head)
        
        # 检查是否吃到食物
        if head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def run(self):
        """运行游戏主循环"""
        while not self.game_over:
            # 处理输入
            key = self.win.getch()
            if key == -1:
                pass
            elif key in [curses.KEY_UP, curses.KEY_DOWN, 
                        curses.KEY_LEFT, curses.KEY_RIGHT]:
                # 防止反向移动
                if (key == curses.KEY_UP and self.direction != curses.KEY_DOWN) or \
                   (key == curses.KEY_DOWN and self.direction != curses.KEY_UP) or \
                   (key == curses.KEY_LEFT and self.direction != curses.KEY_RIGHT) or \
                   (key == curses.KEY_RIGHT and self.direction != curses.KEY_LEFT):
                    self.direction = key
            elif key == ord('q'):  # 按q退出
                break
            
            # 移动蛇
            self.move()
            
            # 绘制游戏
            self.draw()
            
            # 控制游戏速度
            time.sleep(SPEED)
        
        # 游戏结束显示
        if self.game_over:
            game_over_text = f"Game Over! Score: {self.score}"
            self.win.addstr(self.height//2, 
                           (self.width - len(game_over_text))//2,
                           game_over_text)
            self.win.addstr(self.height//2 + 1, 
                           (self.width - 20)//2,
                           "Press any key to exit...")
            self.win.refresh()
            self.win.getch()

def main(stdscr):
    """主函数"""
    # 设置
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()
    
    # 创建并运行游戏
    game = SnakeGame(stdscr)
    game.run()

if __name__ == "__main__":
    # 使用 curses.wrapper 来正确处理终端设置
    curses.wrapper(main) 