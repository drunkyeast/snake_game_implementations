#!/usr/bin/env python3
import pygame
import random
import sys
from enum import Enum

# 游戏常量
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# 颜色定义
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

# 游戏设置
class GameConfig:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    GRID_SIZE = 20
    GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
    GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
    GAME_SPEED = 10  # FPS
    SNAKE_INITIAL_LENGTH = 3

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇 - Pygame版")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        """重置游戏状态"""
        # 初始化蛇的位置（从中间开始）
        center_x = GameConfig.GRID_WIDTH // 2
        center_y = GameConfig.GRID_HEIGHT // 2
        self.snake_body = [(center_x, center_y - i) for i in range(GameConfig.SNAKE_INITIAL_LENGTH)]
        self.snake_direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.game_over = False
        self.generate_food()

    def generate_food(self):
        """生成新的食物"""
        while True:
            food_position = (
                random.randint(0, GameConfig.GRID_WIDTH - 1),
                random.randint(0, GameConfig.GRID_HEIGHT - 1)
            )
            if food_position not in self.snake_body:
                self.food_position = food_position
                break

    def handle_input(self):
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake_direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.snake_direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.snake_direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.snake_direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def update_game_state(self):
        """更新游戏状态"""
        if self.game_over:
            return

        # 更新蛇的方向
        self.snake_direction = self.next_direction

        # 获取蛇头位置
        head_x, head_y = self.snake_body[0]

        # 根据方向移动蛇头
        if self.snake_direction == Direction.UP:
            head_y -= 1
        elif self.snake_direction == Direction.DOWN:
            head_y += 1
        elif self.snake_direction == Direction.LEFT:
            head_x -= 1
        elif self.snake_direction == Direction.RIGHT:
            head_x += 1

        # 检查是否撞墙
        if (head_x < 0 or head_x >= GameConfig.GRID_WIDTH or
            head_y < 0 or head_y >= GameConfig.GRID_HEIGHT):
            self.game_over = True
            return

        # 检查是否撞到自己
        new_head = (head_x, head_y)
        if new_head in self.snake_body:
            self.game_over = True
            return

        # 移动蛇
        self.snake_body.insert(0, new_head)

        # 检查是否吃到食物
        if new_head == self.food_position:
            self.score += 1
            self.generate_food()
        else:
            self.snake_body.pop()

    def draw_game(self):
        """绘制游戏界面"""
        # 清空屏幕
        self.screen.fill(Colors.BLACK)

        # 绘制网格线（可选）
        for x in range(0, GameConfig.WINDOW_WIDTH, GameConfig.GRID_SIZE):
            pygame.draw.line(self.screen, Colors.BLUE, (x, 0), (x, GameConfig.WINDOW_HEIGHT), 1)
        for y in range(0, GameConfig.WINDOW_HEIGHT, GameConfig.GRID_SIZE):
            pygame.draw.line(self.screen, Colors.BLUE, (0, y), (GameConfig.WINDOW_WIDTH, y), 1)

        # 绘制蛇
        for i, (x, y) in enumerate(self.snake_body):
            color = Colors.RED if i == 0 else Colors.GREEN
            rect = pygame.Rect(
                x * GameConfig.GRID_SIZE,
                y * GameConfig.GRID_SIZE,
                GameConfig.GRID_SIZE - 1,
                GameConfig.GRID_SIZE - 1
            )
            pygame.draw.rect(self.screen, color, rect)

        # 绘制食物
        food_rect = pygame.Rect(
            self.food_position[0] * GameConfig.GRID_SIZE,
            self.food_position[1] * GameConfig.GRID_SIZE,
            GameConfig.GRID_SIZE - 1,
            GameConfig.GRID_SIZE - 1
        )
        pygame.draw.rect(self.screen, Colors.YELLOW, food_rect)

        # 显示分数
        score_text = self.font.render(f"得分: {self.score}", True, Colors.WHITE)
        self.screen.blit(score_text, (10, 10))

        # 游戏结束显示
        if self.game_over:
            game_over_text = self.font.render("游戏结束! 按R键重新开始", True, Colors.WHITE)
            text_rect = game_over_text.get_rect(center=(GameConfig.WINDOW_WIDTH/2, GameConfig.WINDOW_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)

        # 更新显示
        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        while True:
            self.handle_input()
            self.update_game_state()
            self.draw_game()
            self.clock.tick(GameConfig.GAME_SPEED)

def main():
    """主函数"""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main() 