import pygame
import random

# Инициализация Pygame
pygame.init()

# экран
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космическое приключение")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# космический корабль
class Spaceship:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 3
        self.boost_speed = 6  # Скорость при ускорении
        self.is_boosting = False  # Флаг ускорения
        self.target_x = self.x  # Целевая позиция по X
        self.target_y = self.y  # Целевая позиция по Y
        self.is_moving_to_target = False  # Флаг движения к точке клика
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Прямоугольник для коллизий

    def draw(self):
        # Рисуем кораблик в виде треугольника
        points = [
            (self.x + self.width // 2, self.y),  # Верхняя точка
            (self.x, self.y + self.height),      # Левая нижняя точка
            (self.x + self.width, self.y + self.height)  # Правая нижняя точка
        ]
        pygame.draw.polygon(screen, BLUE, points)

    def move_towards_target(self):
        if not self.is_moving_to_target:
            return

        # Вычисляем расстояние до цели
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Если корабль близко к цели, останавливаем его
        if distance < self.speed:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving_to_target = False
            return

        # Нормализуем вектор направления
        direction_x = dx / distance
        direction_y = dy / distance

        # Выбираем скорость (обычная или ускоренная)
        current_speed = self.boost_speed if self.is_boosting else self.speed

        # Двигаем корабль
        self.x += direction_x * current_speed
        self.y += direction_y * current_speed

        # Обновляем прямоугольник для коллизий
        self.rect.topleft = (self.x, self.y)

    def move(self, direction):
        current_speed = self.boost_speed if self.is_boosting else self.speed

        if direction == "left" and self.x > 0:
            self.x -= current_speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += current_speed
        if direction == "up" and self.y > 0:
            self.y -= current_speed
        if direction == "down" and self.y < SCREEN_HEIGHT - self.height:
            self.y += current_speed

        # Если корабль управляется клавишами, отключаем движение к точке клика
        self.is_moving_to_target = False

        # Обновляем прямоугольник для коллизий
        self.rect.topleft = (self.x, self.y)

# астероиды
class Asteroid:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(2, 4)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Прямоугольник для коллизий

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)  # Обновляем прямоугольник для коллизий

# Кнопка рестарта
def draw_restart_button():
    font = pygame.font.Font("Romaben-Regular.otf", 28)
    text = font.render("RESTART", True, WHITE)
    button_width = 120
    button_height = 50
    button_x = SCREEN_WIDTH // 2 - button_width - 10  # Сдвигаем влево
    button_y = SCREEN_HEIGHT // 2 - button_height // 2
    pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height))
    screen.blit(text, (button_x + 10, button_y + 10))
    return pygame.Rect(button_x, button_y, button_width, button_height)

# Кнопка выхода
def draw_exit_button():
    font = pygame.font.Font("Romaben-Regular.otf", 28)
    text = font.render("EXIT", True, WHITE)
    button_width = 70
    button_height = 50
    button_x = SCREEN_WIDTH // 2 + 10  # Сдвигаем вправо
    button_y = SCREEN_HEIGHT // 2 - button_height // 2
    pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height))
    screen.blit(text, (button_x + 10, button_y + 10))
    return pygame.Rect(button_x, button_y, button_width, button_height)

# Вывод счёта
def draw_score(score):
    font = pygame.font.Font("Romaben-Regular.otf", 36)
    text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# процесс игры
def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    asteroids = []
    game_over = False
    score = 0
    player_health = 100  # Здоровье игрока

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Обработка нажатия на кнопку рестарта или выхода
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    # Рестарт игры
                    game_over = False
                    spaceship = Spaceship()
                    asteroids = []
                    score = 0
                    player_health = 100
                elif exit_button.collidepoint(mouse_pos):
                    # Выход из игры
                    pygame.quit()
                    return

            # Обработка клика мыши для движения корабля
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                spaceship.target_x = mouse_x - spaceship.width // 2
                spaceship.target_y = mouse_y - spaceship.height // 2
                spaceship.is_moving_to_target = True

        if not game_over:
            # Управление кораблём
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT]:
                spaceship.is_boosting = True
            else:
                spaceship.is_boosting = False

            if keys[pygame.K_a]:
                spaceship.move("left")
            if keys[pygame.K_d]:
                spaceship.move("right")
            if keys[pygame.K_s]:
                spaceship.move("down")
            if keys[pygame.K_w]:
                spaceship.move("up")

            # Движение к точке клика
            spaceship.move_towards_target()

            # Создание новых астероидов
            if random.randint(1, 100) < 5:
                asteroids.append(Asteroid())

            # Очистка экрана
            screen.fill(BLACK)

            # Движение и отрисовка астероидов
            for asteroid in asteroids[:]:
                asteroid.move()
                asteroid.draw()

                # Удаление астероидов, которые улетели за пределы экрана
                if asteroid.y > SCREEN_HEIGHT:
                    asteroids.remove(asteroid)
                    score += 1

                # Проверка столкновения с кораблём
                if spaceship.rect.colliderect(asteroid.rect):
                    player_health -= 10  # Уменьшаем здоровье игрока
                    asteroids.remove(asteroid)  # Удаляем астероид
                    if player_health <= 0:
                        game_over = True

            # Отрисовка корабля
            spaceship.draw()

            # Вывод счёта и здоровья
            draw_score(score)
            font = pygame.font.Font("Romaben-Regular.otf", 36)
            health_text = font.render(f"HP: {player_health}", True, WHITE)
            screen.blit(health_text, (10, 50))

        else:
            # Экран завершения игры
            screen.fill(BLACK)
            draw_score(score)
            restart_button = draw_restart_button()
            exit_button = draw_exit_button()

        # Обновление экрана
        pygame.display.flip()

        # Управление частотой обновления экрана
        clock.tick(60)

# Запуск игры
if __name__ == "__main__":
    main()