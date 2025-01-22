import os
import random
import sqlite3
import pygame

pygame.init()

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1100
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SonicRun")

SONIC_RUNNING = [
    pygame.image.load(os.path.join("Texture/Sonic", "SonicRun1.png")),
    pygame.image.load(os.path.join("Texture/Sonic", "SonicRun2.png"))
]
SONIC_JUMPING = pygame.image.load(os.path.join("Texture/Sonic", "SonicJump.png"))
SONIC_DUCKING = [
    pygame.image.load(os.path.join("Texture/Sonic", "SonicDuck1.png")),
    pygame.image.load(os.path.join("Texture/Sonic", "SonicDuck2.png"))
]

SMALL_OBSTACLES = [
    pygame.image.load(os.path.join("Texture/Barrier", "SmallBarrier1.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "SmallBarrier2.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "SmallBarrier3.png"))
]
LARGE_OBSTACLES = [
    pygame.image.load(os.path.join("Texture/Barrier", "LargeBarrier1.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "LargeBarrier2.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "LargeBarrier3.png"))
]
FLYING_DRAGON = [
    pygame.image.load(os.path.join("Texture/Dragon", "dragon_down.png")),
    pygame.image.load(os.path.join("Texture/Dragon", "dragon_up.png"))
]

SKY_CLOUD = pygame.image.load(os.path.join("Texture/Other", "Cloud.png"))
GAME_BACKGROUND = pygame.image.load(os.path.join("Texture/Other", "Track0.png"))

db_connection = sqlite3.connect("game_scores.db")
db_cursor = db_connection.cursor()
db_cursor.execute(
    "CREATE TABLE IF NOT EXISTS Scores (id INTEGER PRIMARY KEY, score INTEGER)"
)
db_connection.commit()

class SonicCharacter:
    INITIAL_X = 80
    RUNNING_Y = 310
    DUCKING_Y = 340
    JUMP_VELOCITY = 8.5

    def __init__(self):
        self.ducking_images = SONIC_DUCKING
        self.running_images = SONIC_RUNNING
        self.jumping_image = SONIC_JUMPING
        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False
        self.animation_step = 0
        self.vertical_velocity = self.JUMP_VELOCITY
        self.current_image = self.running_images[0]
        self.character_rect = self.current_image.get_rect()
        self.character_rect.x = self.INITIAL_X
        self.character_rect.y = self.RUNNING_Y

    def update(self, input_keys):
        if self.is_ducking:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump()

        if self.animation_step >= 10:
            self.animation_step = 0

        if input_keys[pygame.K_UP] and not self.is_jumping:
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = True
        elif input_keys[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
        elif not (self.is_jumping or input_keys[pygame.K_DOWN]):
            self.is_ducking = False
            self.is_running = True
            self.is_jumping = False

    def duck(self):
        self.current_image = self.ducking_images[self.animation_step // 5]
        self.character_rect = self.current_image.get_rect()
        self.character_rect.x = self.INITIAL_X
        self.character_rect.y = self.DUCKING_Y
        self.animation_step += 1

    def run(self):
        self.current_image = self.running_images[self.animation_step // 5]
        self.character_rect = self.current_image.get_rect()
        self.character_rect.x = self.INITIAL_X
        self.character_rect.y = self.RUNNING_Y
        self.animation_step += 1

    def jump(self):
        self.current_image = self.jumping_image
        if self.is_jumping:
            self.character_rect.y -= self.vertical_velocity * 4
            self.vertical_velocity -= 0.8
        if self.vertical_velocity < -self.JUMP_VELOCITY:
            self.is_jumping = False
            self.vertical_velocity = self.JUMP_VELOCITY

    def draw(self, WINDOW):
        WINDOW.blit(self.current_image, (self.character_rect.x, self.character_rect.y))

class SkyCloud:
    def __init__(self):
        self.x_position = WINDOW_WIDTH + random.randint(800, 1000)
        self.y_position = random.randint(50, 100)
        self.cloud_image = SKY_CLOUD
        self.cloud_width = self.cloud_image.get_width()

    def update(self):
        self.x_position -= game_speed
        if self.x_position < -self.cloud_width:
            self.x_position = WINDOW_WIDTH + random.randint(2500, 3000)
            self.y_position = random.randint(50, 100)

    def draw(self, WINDOW):
        WINDOW.blit(self.cloud_image, (self.x_position, self.y_position))

class Obstacle:
    def __init__(self, images, obstacle_type):
        self.images = images
        self.obstacle_type = obstacle_type
        self.obstacle_rect = self.images[self.obstacle_type].get_rect()
        self.obstacle_rect.x = WINDOW_WIDTH

    def update(self):
        self.obstacle_rect.x -= game_speed
        if self.obstacle_rect.x < -self.obstacle_rect.width:
            obstacle_list.pop()

    def draw(self, WINDOW):
        WINDOW.blit(self.images[self.obstacle_type], self.obstacle_rect)

class SmallObstacle(Obstacle):
    def __init__(self, images):
        self.obstacle_type = random.randint(0, 2)
        super().__init__(images, self.obstacle_type)
        self.obstacle_rect.y = 325

class LargeObstacle(Obstacle):
    def __init__(self, images):
        self.obstacle_type = random.randint(0, 2)
        super().__init__(images, self.obstacle_type)
        self.obstacle_rect.y = 300

class FlyingDragon(Obstacle):
    def __init__(self, images):
        self.obstacle_type = 0
        super().__init__(images, self.obstacle_type)
        self.obstacle_rect.y = 250
        self.animation_index = 0

    def draw(self, WINDOW):
        if self.animation_index >= 9:
            self.animation_index = 0
        WINDOW.blit(self.images[self.animation_index // 5], self.obstacle_rect)
        self.animation_index += 1

def main_game():
    global game_speed, background_x_position, background_y_position, current_score, obstacle_list
    is_running = True
    game_clock = pygame.time.Clock()
    player_character = SonicCharacter()
    background_cloud = SkyCloud()
    game_speed = 20
    background_x_position = 0
    background_y_position = 380
    current_score = 0
    font_style = pygame.font.Font('freesansbold.ttf', 20)
    obstacle_list = []
    death_count = 0

    def update_score():
        global current_score, game_speed
        current_score += 1
        if current_score % 100 == 0:
            game_speed += 1

        score_text = font_style.render("Очки: " + str(current_score), True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.center = (100, 40)
        WINDOW.blit(score_text, score_rect)

    def draw_background():
        global background_x_position, background_y_position
        background_width = GAME_BACKGROUND.get_width()
        WINDOW.blit(GAME_BACKGROUND, (background_x_position, background_y_position))
        WINDOW.blit(GAME_BACKGROUND, (background_width + background_x_position, background_y_position))
        if background_x_position <= -background_width:
            background_x_position = 0
        background_x_position -= game_speed

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        WINDOW.fill((0, 137, 255))
        player_input = pygame.key.get_pressed()

        player_character.draw(WINDOW)
        player_character.update(player_input)

        if len(obstacle_list) == 0:
            random_choice = random.randint(0, 2)
            if random_choice == 0:
                obstacle_list.append(SmallObstacle(SMALL_OBSTACLES))
            elif random_choice == 1:
                obstacle_list.append(LargeObstacle(LARGE_OBSTACLES))
            elif random_choice == 2:
                obstacle_list.append(FlyingDragon(FLYING_DRAGON))

        for obstacle in obstacle_list:
            obstacle.draw(WINDOW)
            obstacle.update()
            if player_character.character_rect.colliderect(obstacle.obstacle_rect):
                pygame.time.delay(2000)
                death_count += 1
                save_score_to_database(current_score)
                main_menu(death_count)

        draw_background()

        background_cloud.draw(WINDOW)
        background_cloud.update()

        update_score()

        game_clock.tick(30)
        pygame.display.update()

def main_menu(death_count):
    global current_score
    is_running = True
    while is_running:
        WINDOW.fill((0, 239, 200))
        font_style = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            start_text = font_style.render("Нажмите любую кнопку чтобы начать", True, (0, 0, 0))
        else:
            start_text = font_style.render("Нажмите любую кнопку чтобы рестартнуть", True, (0, 0, 0))
            final_score_text = font_style.render(f"Твой результат: {current_score}", True, (0, 0, 0))
            high_score_text = font_style.render(f"Лучший результат: {get_high_score()}", True, (0, 0, 0))

            final_score_rect = final_score_text.get_rect()
            high_score_rect = high_score_text.get_rect()
            final_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            high_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
            WINDOW.blit(final_score_text, final_score_rect)
            WINDOW.blit(high_score_text, high_score_rect)

        start_text_rect = start_text.get_rect()
        start_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        WINDOW.blit(start_text, start_text_rect)
        WINDOW.blit(SONIC_RUNNING[0], (WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
            if event.type == pygame.KEYDOWN:
                main_game()

main_menu(death_count=0)

db_connection.close()
