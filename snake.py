# -*- coding: utf-8 -*-
"""
贪吃蛇游戏 (Snake)
操作：方向键控制移动，空格暂停/继续，R 键重新开始
运行：python snake.py
"""
import random
import tkinter as tk

# ---------- 配置 ----------
CELL = 24                # 格子像素
COLS, ROWS = 24, 24      # 棋盘格数
SPEED = 120              # 移动间隔(ms)，越小越快
BG = "#1e1e2e"
GRID_BG = "#2a2a3c"
SNAKE_HEAD = "#7cffb2"
SNAKE_BODY = "#3ecf8e"
FOOD = "#ff6b6b"
TEXT = "#e6e6e6"


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("贪吃蛇 Snake")
        root.resizable(False, False)

        self.canvas = tk.Canvas(
            root, width=COLS * CELL, height=ROWS * CELL,
            bg=BG, highlightthickness=0,
        )
        self.canvas.pack()

        self.status = tk.Label(
            root, text="方向键移动 | 空格暂停 | R 重开",
            bg=BG, fg=TEXT, font=("Microsoft YaHei", 11),
        )
        self.status.pack(fill="x")

        # 绑定按键
        root.bind("<Up>", lambda e: self.set_dir(0, -1))
        root.bind("<Down>", lambda e: self.set_dir(0, 1))
        root.bind("<Left>", lambda e: self.set_dir(-1, 0))
        root.bind("<Right>", lambda e: self.set_dir(1, 0))
        root.bind("<space>", lambda e: self.toggle_pause())
        root.bind("<KeyPress-r>", lambda e: self.reset())

        self.reset()

    # ---------- 状态 ----------
    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]  # 头在前
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.paused = False
        self.game_over = False
        self.place_food()
        self.draw()
        self.tick()

    def place_food(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.snake:
                self.food = pos
                return

    # ---------- 控制 ----------
    def set_dir(self, dx, dy):
        # 禁止直接掉头
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return
        self.next_direction = (dx, dy)

    def toggle_pause(self):
        if self.game_over:
            return
        self.paused = not self.paused
        self.draw()

    # ---------- 主循环 ----------
    def tick(self):
        if self.game_over:
            return
        if not self.paused:
            self.step()
        self.root.after(SPEED, self.tick)

    def step(self):
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]

        # 撞墙
        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            self.end_game()
            return
        # 撞到自己（尾巴这一步会移走，但简化处理：除尾外不算安全）
        if (nx, ny) in self.snake[:-1]:
            self.end_game()
            return

        self.snake.insert(0, (nx, ny))

        if (nx, ny) == self.food:
            self.score += 10
            self.place_food()
        else:
            self.snake.pop()

        self.draw()

    def end_game(self):
        self.game_over = True
        self.draw()

    # ---------- 绘制 ----------
    def draw_cell(self, x, y, color, pad=1):
        x0, y0 = x * CELL + pad, y * CELL + pad
        x1, y1 = (x + 1) * CELL - pad, (y + 1) * CELL - pad
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def draw(self):
        self.canvas.delete("all")
        # 食物
        fx, fy = self.food
        self.canvas.create_oval(
            fx * CELL + 3, fy * CELL + 3,
            (fx + 1) * CELL - 3, (fy + 1) * CELL - 3,
            fill=FOOD, outline="",
        )
        # 蛇
        for i, (x, y) in enumerate(self.snake):
            self.draw_cell(x, y, SNAKE_HEAD if i == 0 else SNAKE_BODY)

        msg = f"得分：{self.score}"
        if self.paused:
            msg += "    [已暂停]"
        if self.game_over:
            self.canvas.create_text(
                COLS * CELL // 2, ROWS * CELL // 2 - 20,
                text="游戏结束", fill=FOOD,
                font=("Microsoft YaHei", 28, "bold"),
            )
            self.canvas.create_text(
                COLS * CELL // 2, ROWS * CELL // 2 + 20,
                text=f"本局得分 {self.score}，按 R 重新开始",
                fill=TEXT, font=("Microsoft YaHei", 14),
            )
        self.status.config(text=f"{msg}    |    方向键移动 · 空格暂停 · R 重开")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
