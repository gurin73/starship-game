import pygame

BLUE = (0, 0, 255)
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

class Spaceship:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 3
        self.boost_speed = 6
        self.is_boosting = False
        self.target_x = self.x
        self.target_y = self.y
        self.is_moving_to_target = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        points = [(self.x + self.width // 2, self.y),
                  (self.x, self.y + self.height),
                  (self.x + self.width, self.y + self.height)]
        pygame.draw.polygon(screen, BLUE, points)

    def move_towards_target(self):
        if not self.is_moving_to_target:
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.speed:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving_to_target = False
            return

        direction_x = dx / distance
        direction_y = dy / distance

        current_speed = self.boost_speed if self.is_boosting else self.speed

        self.x += direction_x * current_speed
        self.y += direction_y * current_speed

        self.rect.topleft = (self.x, self.y)

    def move(self, direction):  # <-- Добавил этот метод
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
