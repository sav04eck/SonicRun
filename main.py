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