import os
import random
import sqlite3
import pygame

pygame.init()

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1100
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

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