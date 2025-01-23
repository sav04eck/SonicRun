# Импорт необходимых библиотек
import os  # модуль для работы с файловой системой
import random  # модуль для генерации случайных чисел
import sqlite3  # библиотека для работы с базами данных SQLite

import pygame  # библиотека для создания игр

pygame.init()  # инициализация всех модулей Pygame

# Глобальные константы
WINDOW_HEIGHT = 600  # высота окна игры
WINDOW_WIDTH = 1100  # ширина окна игры
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # создание игрового окна

# Загрузка изображений для анимации Соника
SONIC_RUNNING = [  # кадры анимации бега
    pygame.image.load(os.path.join("Texture/Sonic", "SonicRun1.png")),
    pygame.image.load(os.path.join("Texture/Sonic", "SonicRun2.png"))
]
SONIC_JUMPING = pygame.image.load(os.path.join("Texture/Sonic", "SonicJump.png"))  # изображение прыжка
SONIC_DUCKING = [  # кадры анимации приседания
    pygame.image.load(os.path.join("Texture/Sonic", "SonicDuck1.png")),
    pygame.image.load(os.path.join("Texture/Sonic", "SonicDuck2.png"))
]
SONIC_START = pygame.image.load(os.path.join("Texture/Sonic", "SonicStart.png"))  # изображение для меню

# Загрузка изображений препятствий
SMALL_OBSTACLES = [  # небольшие препятствия
    pygame.image.load(os.path.join("Texture/Barrier", "SmallBarrier1.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "SmallBarrier2.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "SmallBarrier3.png"))
]
LARGE_OBSTACLES = [  # большие препятствия
    pygame.image.load(os.path.join("Texture/Barrier", "LargeBarrier1.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "LargeBarrier2.png")),
    pygame.image.load(os.path.join("Texture/Barrier", "LargeBarrier3.png"))
]
FLYING_DRAGON = [  # изображения анимации летающего дракона
    pygame.image.load(os.path.join("Texture/Dragon", "dragon_down.png")),
    pygame.image.load(os.path.join("Texture/Dragon", "dragon_up.png"))
]

# Загрузка облаков и фона
SKY_CLOUD = pygame.image.load(os.path.join("Texture/Other", "Cloud.png"))  # изображение облака
GAME_BACKGROUND = pygame.image.load(os.path.join("Texture/Other", "Track0.png"))  # изображение фона

# Настройка базы данных
db_connection = sqlite3.connect("game_scores.db")  # подключение к базе данных
db_cursor = db_connection.cursor()  # создание курсора для работы с БД
db_cursor.execute(  # создание таблицы для хранения результатов
    "CREATE TABLE IF NOT EXISTS Scores (id INTEGER PRIMARY KEY, score INTEGER)"
)
db_connection.commit()  # сохранение изменений в БД


# Класс персонажа Соник
class SonicCharacter:
    INITIAL_X = 80  # начальная позиция X
    RUNNING_Y = 310  # позиция Y для бега
    DUCKING_Y = 340  # позиция Y для приседания
    JUMP_VELOCITY = 8.5  # начальная скорость прыжка

    def __init__(self):
        # Инициализация изображений
        self.ducking_images = SONIC_DUCKING
        self.running_images = SONIC_RUNNING
        self.jumping_image = SONIC_JUMPING

        # Состояния персонажа
        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False

        self.animation_step = 0  # шаг анимации
        self.vertical_velocity = self.JUMP_VELOCITY  # скорость по вертикали
        self.current_image = self.running_images[0]  # текущее изображение
        self.character_rect = self.current_image.get_rect()  # прямоугольник для коллизий
        self.character_rect.x = self.INITIAL_X
        self.character_rect.y = self.RUNNING_Y

    # Обновление состояния персонажа
    def update(self, input_keys):
        # Выбор действия в зависимости от состояния
        if self.is_ducking:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump()

        if self.animation_step >= 10:  # сброс анимации
            self.animation_step = 0

        # Обработка ввода пользователя
        if input_keys[pygame.K_UP] and not self.is_jumping:  # прыжок
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = True
        elif input_keys[pygame.K_DOWN] and not self.is_jumping:  # приседание
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
        elif not (self.is_jumping or input_keys[pygame.K_DOWN]):  # бег
            self.is_ducking = False
            self.is_running = True
            self.is_jumping = False

    # Действия персонажа
    def duck(self):  # приседание
        self.current_image = self.ducking_images[self.animation_step // 5]
        self.character_rect = self.current_image.get_rect()
        self.character_rect.x = self.INITIAL_X
        self.character_rect.y = self.DUCKING_Y
        self.animation_step += 1

    def run(self):  # бег
        self.current_image = self.running_images[self.animation_step // 5]
        self.character_rect = self.current_image.get_rect()
        self.character_rect.x = self.INITIAL_X
        self.character_rect.y = self.RUNNING_Y
        self.animation_step += 1

    def jump(self):  # прыжок
        self.current_image = self.jumping_image
        if self.is_jumping:
            self.character_rect.y -= self.vertical_velocity * 4
            self.vertical_velocity -= 0.8
        if self.vertical_velocity < -self.JUMP_VELOCITY:  # завершение прыжка
            self.is_jumping = False
            self.vertical_velocity = self.JUMP_VELOCITY

    # Отображение персонажа
    def draw(self, WINDOW):
        WINDOW.blit(self.current_image, (self.character_rect.x, self.character_rect.y))


# Класс облаков на фоне
class SkyCloud:
    def __init__(self):
        self.x_position = WINDOW_WIDTH + random.randint(800, 1000)  # начальная позиция X (за экраном)
        self.y_position = random.randint(50, 100)  # случайная позиция Y
        self.cloud_image = SKY_CLOUD  # изображение облака
        self.cloud_width = self.cloud_image.get_width()  # ширина изображения облака

    # Обновление позиции облака (движение влево)
    def update(self):
        self.x_position -= game_speed  # движение облака влево
        if self.x_position < -self.cloud_width:  # если облако ушло за экран
            # Задаем новое случайное положение облака
            self.x_position = WINDOW_WIDTH + random.randint(2500, 3000)
            self.y_position = random.randint(50, 100)

    # Отображение облака на экране
    def draw(self, WINDOW):
        WINDOW.blit(self.cloud_image, (self.x_position, self.y_position))


# Базовый класс препятствий
class Obstacle:
    def __init__(self, images, obstacle_type):
        self.images = images  # список изображений препятствия
        self.obstacle_type = obstacle_type  # тип препятствия (индекс изображения)
        self.obstacle_rect = self.images[self.obstacle_type].get_rect()  # прямоугольник для коллизий
        self.obstacle_rect.x = WINDOW_WIDTH  # начальная позиция X (за экраном)

    # Обновление позиции препятствия
    def update(self):
        self.obstacle_rect.x -= game_speed  # движение препятствия влево
        if self.obstacle_rect.x < -self.obstacle_rect.width:  # если препятствие ушло за экран
            obstacle_list.pop()  # удаление препятствия из списка

    # Отображение препятствия на экране
    def draw(self, WINDOW):
        WINDOW.blit(self.images[self.obstacle_type], self.obstacle_rect)


# Класс для небольших препятствий
class SmallObstacle(Obstacle):
    def __init__(self, images):
        self.obstacle_type = random.randint(0, 2)  # случайный выбор типа препятствия
        super().__init__(images, self.obstacle_type)
        self.obstacle_rect.y = 325  # фиксированная высота для небольших препятствий


# Класс для больших препятствий
class LargeObstacle(Obstacle):
    def __init__(self, images):
        self.obstacle_type = random.randint(0, 2)  # случайный выбор типа препятствия
        super().__init__(images, self.obstacle_type)
        self.obstacle_rect.y = 300  # фиксированная высота для больших препятствий


# Класс для летающих драконов
class FlyingDragon(Obstacle):
    def __init__(self, images):
        self.obstacle_type = 0  # фиксированный тип изображения для дракона
        super().__init__(images, self.obstacle_type)
        self.obstacle_rect.y = 250  # фиксированная высота для дракона
        self.animation_index = 0  # индекс текущего кадра анимации

    # Отображение анимации дракона
    def draw(self, WINDOW):
        if self.animation_index >= 9:  # сброс индекса анимации
            self.animation_index = 0
        # Отображение текущего кадра анимации
        WINDOW.blit(self.images[self.animation_index // 5], self.obstacle_rect)
        self.animation_index += 1


# Главная игровая функция
def main_game():
    global game_speed, background_x_position, background_y_position, current_score, obstacle_list
    is_running = True  # флаг работы игры
    game_clock = pygame.time.Clock()  # создание объекта для управления FPS
    player_character = SonicCharacter()  # создание персонажа
    background_cloud = SkyCloud()  # создание облака
    game_speed = 20  # начальная скорость игры
    background_x_position = 0  # начальная позиция фона
    background_y_position = 380  # фиксированная позиция фона по Y
    current_score = 0  # текущий счет
    font_style = pygame.font.Font('freesansbold.ttf', 20)  # шрифт для текста
    obstacle_list = []  # список препятствий
    death_count = 0  # количество смертей

    # Функция для обновления счета
    def update_score():
        global current_score, game_speed
        current_score += 1  # увеличение счета
        if current_score % 100 == 0:  # увеличение скорости каждые 100 очков
            game_speed += 1

        # Отображение счета на экране
        score_text = font_style.render(str(current_score), True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.center = (50, 40)
        WINDOW.blit(score_text, score_rect)

    # Функция для отображения фона
    def draw_background():
        global background_x_position, background_y_position
        background_width = GAME_BACKGROUND.get_width()  # ширина фонового изображения
        # Отображение двух частей фона, чтобы создать бесшовный эффект
        WINDOW.blit(GAME_BACKGROUND, (background_x_position, background_y_position))
        WINDOW.blit(GAME_BACKGROUND, (background_width + background_x_position, background_y_position))
        if background_x_position <= -background_width:  # сброс положения фона
            background_x_position = 0
        background_x_position -= game_speed  # движение фона влево

    while is_running:  # главный игровой цикл
        for event in pygame.event.get():  # обработка событий
            if event.type == pygame.QUIT:  # выход из игры
                is_running = False

        WINDOW.fill((0, 137, 255))  # заполнение экрана белым цветом
        player_input = pygame.key.get_pressed()  # получение нажатий клавиш

        # Обновление и отображение персонажа
        player_character.draw(WINDOW)
        player_character.update(player_input)

        # Создание препятствий, если их нет
        if len(obstacle_list) == 0:
            random_choice = random.randint(0, 2)
            if random_choice == 0:
                obstacle_list.append(SmallObstacle(SMALL_OBSTACLES))
            elif random_choice == 1:
                obstacle_list.append(LargeObstacle(LARGE_OBSTACLES))
            elif random_choice == 2:
                obstacle_list.append(FlyingDragon(FLYING_DRAGON))

        # Обновление и отображение препятствий
        for obstacle in obstacle_list:
            obstacle.draw(WINDOW)
            obstacle.update()
            if player_character.character_rect.colliderect(obstacle.obstacle_rect):  # проверка на столкновение
                pygame.time.delay(2000)  # пауза при смерти
                death_count += 1
                save_score_to_database(current_score)  # сохранение результата
                main_menu(death_count)  # возврат в главное меню

        draw_background()  # отображение фона

        background_cloud.draw(WINDOW)  # отображение облаков
        background_cloud.update()  # обновление их позиции

        update_score()  # обновление и отображение счета

        game_clock.tick(30)  # ограничение FPS
        pygame.display.update()  # обновление экрана


# Функция для сохранения результата в базу данных
def save_score_to_database(score):
    db_cursor.execute("INSERT INTO Scores (score) VALUES (?)", (score,))  # добавление результата в таблицу
    db_connection.commit()  # сохранение изменений в базе данных


# Функция для получения рекорда из базы данных
def get_high_score():
    db_cursor.execute("SELECT MAX(score) FROM Scores")  # получение максимального значения из столбца score
    high_score = db_cursor.fetchone()[0]  # извлечение результата из курсора
    return high_score if high_score else 0  # если рекорда нет, возвращается 0


# Главное меню игры
def main_menu(death_count):
    global current_score
    is_running = True  # флаг работы меню
    while is_running:
        WINDOW.fill((0, 0, 0))  # заполнение экрана черным цветом
        font_style = pygame.font.Font('freesansbold.ttf', 30)  # шрифт для текста

        # Отображение текста в зависимости от количества смертей
        if death_count == 0:
            start_text = font_style.render("Нажмите любую кнопку чтобы начать", True, (255, 255, 255))
        else:
            start_text = font_style.render("Нажмите любую кнопку чтобы рестартнуть", True, (255, 255, 255))
            final_score_text = font_style.render(f"Твой результат: {current_score}", True,
                                                 (255, 255, 255))  # вывод счета
            high_score_text = font_style.render(f"Лучший результат: {get_high_score()}", True,
                                                (255, 255, 255))  # вывод рекорда

            # Позиционирование текста на экране
            final_score_rect = final_score_text.get_rect()
            high_score_rect = high_score_text.get_rect()
            final_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            high_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
            WINDOW.blit(final_score_text, final_score_rect)  # отображение текста результата
            WINDOW.blit(high_score_text, high_score_rect)  # отображение текста рекорда

        # Отображение основного текста (начало или рестарт)
        start_text_rect = start_text.get_rect()
        start_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        WINDOW.blit(start_text, start_text_rect)
        WINDOW.blit(SONIC_START, (WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT // 2 - 140))  # отображение персонажа
        pygame.display.update()  # обновление экрана

        for event in pygame.event.get():  # обработка событий
            if event.type == pygame.QUIT:  # выход из игры
                pygame.quit()
                is_running = False
            if event.type == pygame.KEYDOWN:  # начало игры при нажатии клавиши
                main_game()  # запуск основной игры


# Запуск главного меню при старте программы
main_menu(death_count=0)

# Закрытие подключения к базе данных
db_connection.close()
