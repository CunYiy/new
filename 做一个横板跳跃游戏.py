import pygame
import random

# ===================== 全局常量配置 =====================
SCREEN_WIDTH = 800    # 屏幕宽度
SCREEN_HEIGHT = 600   # 屏幕高度
LEVEL_WIDTH = 2400    # 关卡总宽度（比屏幕宽，实现相机滚动）
GRAVITY = 0.8         # 重力加速度
JUMP_FORCE = -16      # 跳跃力度
PLAYER_SPEED = 5      # 移动速度
MAX_HP = 3            # 玩家最大血量
INVINCIBLE_FRAMES = 60# 受伤后无敌帧数（60帧≈1秒）
COIN_COUNT = 15       # 金币数量
ENEMY_COUNT = 5       # 敌人数量

# ===================== 相机类（核心：实现镜头跟随） =====================
class Camera:
    def __init__(self, level_width):
        self.offset_x = 0
        self.level_width = level_width

    def update(self, player):
        # 让玩家保持在屏幕水平中间位置
        target_x = player.rect.centerx - SCREEN_WIDTH // 2
        # 限制相机不超出关卡左右边界，防止看到空白区域
        self.offset_x = max(0, min(target_x, self.level_width - SCREEN_WIDTH))

    def apply(self, entity_rect):
        """把世界坐标转换成屏幕坐标：实体位置 - 相机偏移量"""
        return entity_rect.move(-self.offset_x, 0)

# ===================== 玩家类（新增：动画、血量、无敌） =====================
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)  # 用Rect统一管理位置和碰撞
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        # 血量与无敌状态
        self.hp = MAX_HP
        self.invincible_timer = 0  # 无敌倒计时，大于0时不会受伤

        # ========== 角色动画帧（代码生成，可替换为图片） ==========
        # 站立帧
        self.stand_frame = pygame.Surface((40, 60))
        self.stand_frame.fill((0, 120, 255))
        # 跑步动画2帧，用色块差异模拟跑步动作
        self.run_frames = []
        for i in range(2):
            frame = pygame.Surface((40, 60))
            frame.fill((0, 150, 255))
            # 绘制腿部差异，区分两帧
            pygame.draw.rect(frame, (0, 80, 180), (5 + i*15, 50, 12, 10))
            self.run_frames.append(frame)
        # 跳跃帧
        self.jump_frame = pygame.Surface((40, 60))
        self.jump_frame.fill((255, 140, 0))

        # 动画状态控制
        self.anim_state = "stand"  # stand/run/jump
        self.anim_index = 0
        self.anim_timer = 0

    def update(self, platforms):
        # 1. 键盘输入控制水平移动
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED

        # 2. 应用重力
        self.vel_y += GRAVITY

        # 3. 水平移动 + 关卡边界限制
        self.rect.x += self.vel_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH

        # 4. 垂直移动 + 平台碰撞检测
        self.rect.y += self.vel_y
        self.on_ground = False

        for plat in platforms:
            # 水平方向重叠 且 向下掉落 且 底部碰到平台顶面 → 判定站在平台上
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0 and self.rect.bottom <= plat.rect.top + 10:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # 5. 无敌时间倒计时
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # 6. 更新动画状态
        if not self.on_ground:
            self.anim_state = "jump"
        elif abs(self.vel_x) > 0:
            self.anim_state = "run"
            # 每10帧切换一次跑步帧
            self.anim_timer += 1
            if self.anim_timer >= 10:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.run_frames)
        else:
            self.anim_state = "stand"

    def jump(self):
        """只有在地面才能跳跃，禁止二段跳"""
        if self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False
            return True  # 返回跳跃成功，用于播放音效
        return False

    def take_damage(self):
        """受伤逻辑：无敌状态下不扣血"""
        if self.invincible_timer <= 0:
            self.hp -= 1
            self.invincible_timer = INVINCIBLE_FRAMES
            # 受伤后向上弹一下，增加手感
            self.vel_y = -8
            return True
        return False

    def get_current_frame(self):
        """根据当前状态返回对应的动画帧"""
        if self.anim_state == "jump":
            return self.jump_frame
        elif self.anim_state == "run":
            return self.run_frames[self.anim_index]
        else:
            return self.stand_frame

    def draw(self, screen, camera):
        # 无敌期间闪烁显示
        if self.invincible_timer > 0 and self.invincible_timer % 6 < 3:
            return  # 每隔几帧不画，实现闪烁效果
        screen_rect = camera.apply(self.rect)
        screen.blit(self.get_current_frame(), screen_rect)

# ===================== 平台类 =====================
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)
        pygame.draw.rect(screen, (0, 180, 100), screen_rect)

# ===================== 金币类（碰撞加分） =====================
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False  # 是否已被收集

    def draw(self, screen, camera):
        if not self.collected:
            screen_rect = camera.apply(self.rect)
            # 绘制黄色圆形金币
            pygame.draw.circle(screen, (255, 215, 0), screen_rect.center, 10)

# ===================== 敌人类（左右巡逻，碰到扣血） =====================
class Enemy:
    def __init__(self, x, y, patrol_left, patrol_right):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.patrol_left = patrol_left    # 巡逻左边界
        self.patrol_right = patrol_right  # 巡逻右边界
        self.speed = 2
        self.direction = 1  # 1=向右，-1=向左

    def update(self):
        # 左右巡逻，碰到边界掉头
        self.rect.x += self.speed * self.direction
        if self.rect.left <= self.patrol_left or self.rect.right >= self.patrol_right:
            self.direction *= -1

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)
        pygame.draw.rect(screen, (220, 30, 60), screen_rect)

# ===================== 音效加载（兼容无文件情况） =====================
def load_sound(file_path):
    try:
        return pygame.mixer.Sound(file_path)
    except:
        # 没有音频文件也不报错，返回空
        return None

# ===================== 游戏主逻辑 =====================
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("横版跳跃完整版")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # 用于显示分数和血量

    # 加载音效（把音频文件放在项目目录下即可生效）
    jump_sound = load_sound("jump.wav")
    coin_sound = load_sound("coin.wav")

    # 创建相机
    camera = Camera(LEVEL_WIDTH)

    # 创建玩家
    player = Player(100, 400)
    score = 0

    # 创建平台（分布在整个关卡中）
    platforms = [
        # 地面（贯穿整个关卡）
        Platform(0, 550, LEVEL_WIDTH, 50),
        # 空中平台
        Platform(150, 450, 120, 20),
        Platform(350, 380, 120, 20),
        Platform(550, 300, 120, 20),
        Platform(800, 420, 150, 20),
        Platform(1050, 350, 100, 20),
        Platform(1300, 280, 120, 20),
        Platform(1550, 400, 150, 20),
        Platform(1800, 320, 100, 20),
        Platform(2050, 250, 150, 20),
        Platform(2200, 450, 120, 20),
    ]

    # 随机生成金币
    coins = []
    for _ in range(COIN_COUNT):
        x = random.randint(100, LEVEL_WIDTH - 100)
        y = random.randint(100, 500)
        coins.append(Coin(x, y))

    # 生成敌人（在各自区域巡逻）
    enemies = [
        Enemy(200, 510, 150, 400),
        Enemy(600, 510, 500, 900),
        Enemy(1100, 510, 1000, 1400),
        Enemy(1600, 510, 1500, 1900),
        Enemy(2100, 510, 2000, 2300),
    ]

    running = True
    while running:
        # ---------- 事件处理 ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if player.jump() and jump_sound:
                        jump_sound.play()  # 跳跃成功播放音效

        # ---------- 逻辑更新 ----------
        player.update(platforms)
        camera.update(player)  # 相机跟随玩家更新

        # 更新敌人 + 碰撞扣血
        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                player.take_damage()

        # 金币碰撞检测
        for coin in coins:
            if not coin.collected and player.rect.colliderect(coin.rect):
                coin.collected = True
                score += 10
                if coin_sound:
                    coin_sound.play()  # 收集金币播放音效

        # 掉出地图重置
        if player.rect.top > SCREEN_HEIGHT:
            player.rect.x = 100
            player.rect.y = 400
            player.vel_y = 0
            player.hp = max(1, player.hp - 1)  # 掉下去扣1血

        # 血量归零重置游戏
        if player.hp <= 0:
            score = 0
            player.hp = MAX_HP
            player.rect.x = 100
            player.rect.y = 400
            # 重置所有金币
            for coin in coins:
                coin.collected = False

        # ---------- 画面绘制 ----------
        screen.fill((30, 30, 30))  # 深灰背景

        # 绘制平台、金币、敌人、玩家（都需要应用相机偏移）
        for plat in platforms:
            plat.draw(screen, camera)
        for coin in coins:
            coin.draw(screen, camera)
        for enemy in enemies:
            enemy.draw(screen, camera)
        player.draw(screen, camera)

        # ---------- UI界面（固定在屏幕上，不需要相机偏移） ----------
        score_text = font.render(f"分数: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        hp_text = font.render(f"血量: {player.hp}", True, (255, 80, 80))
        screen.blit(hp_text, (20, 60))

        pygame.display.flip()
        clock.tick(60)  # 锁定60帧

    pygame.quit()

if __name__ == "__main__":
    main()

