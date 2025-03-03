import pygame
import random
from spaceship import Spaceship
from asteroid import Asteroid
from buttons import draw_restart_button, draw_exit_button
from utils import draw_score

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космическое приключение")

pygame.mixer.music.load("BONES - MyOwnPersonalHell.mp3")

BLACK = (0, 0, 0)

def draw_health(screen, health):
    font = pygame.font.Font("Romaben-Regular.otf", 36)
    text = font.render(f"HP: {health}", True, (255, 255, 255))
    screen.blit(text, (10, 50))

def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    asteroids = [Asteroid() for _ in range(5)]  # Начальные астероиды
    score = 0
    health = 100  # Количество жизней
    running = True
    game_over = False  # Флаг завершения игры
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.25)

    keys = {"left": False, "right": False, "up": False, "down": False}

    while running:
        screen.fill(BLACK)

        if not game_over:
            # Двигаем корабль в зависимости от нажатых клавиш
            if keys["left"]:
                spaceship.move("left")
            if keys["right"]:
                spaceship.move("right")
            if keys["up"]:
                spaceship.move("up")
            if keys["down"]:
                spaceship.move("down")

            spaceship.draw(screen)
            spaceship.move_towards_target()

            # Создание новых астероидов
            if random.randint(1, 100) < 3:
                asteroids.append(Asteroid())

            # Работа с астероидами
            for asteroid in asteroids[:]:  # Используем [:], чтобы безопасно изменять список
                asteroid.move()
                asteroid.draw(screen)

                # Проверка столкновений
                if spaceship.rect.colliderect(asteroid.rect):
                    health -= 10  # Уменьшаем жизни
                    asteroids.remove(asteroid)  # Удаляем астероид после столкновения
                    asteroids.append(Asteroid())  # Спавним новый

                # Удаляем астероиды, если они вышли за экран, и добавляем новые
                if asteroid.y > SCREEN_HEIGHT:
                    score += 1  # Увеличиваем счет за пролетевший астероид
                    asteroids.remove(asteroid)
                    asteroids.append(Asteroid())

            draw_score(screen, score)  # Отображаем счет
            draw_health(screen, health)  # Отображаем HP

            # Проверка на проигрыш
            if health <= 0:
                game_over = True  # Игра завершена
                pygame.mixer.music.stop()  # Останавливаем музыку

        else:
            # Экран завершения игры
            draw_score(screen, score)  # Отображаем счет
            restart_button = draw_restart_button(screen)  # Кнопка рестарта
            exit_button = draw_exit_button(screen)  # Кнопка выхода

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обработка кликов по кнопкам (только если игра завершена)
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    # Рестарт игры
                    game_over = False
                    spaceship = Spaceship()
                    asteroids = [Asteroid() for _ in range(5)]
                    score = 0
                    health = 100
                    pygame.mixer.music.play(-1)  # Запускаем музыку заново
                    pygame.mixer.music.set_volume(0.25)
                elif exit_button.collidepoint(mouse_pos):
                    # Выход из игры
                    running = False

            # Движение по клику
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Учитываем центр корабля при задании целевых координат
                spaceship.target_x = mouse_x - spaceship.width // 2
                spaceship.target_y = mouse_y - spaceship.height // 2
                spaceship.is_moving_to_target = True

            # Обрабатываем нажатие клавиш WSAD
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    keys["left"] = True
                if event.key == pygame.K_d:
                    keys["right"] = True
                if event.key == pygame.K_w:
                    keys["up"] = True
                if event.key == pygame.K_s:
                    keys["down"] = True
                if event.key == pygame.K_LSHIFT:  # Ускорение
                    spaceship.is_boosting = True

            # Обрабатываем отпускание клавиш
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    keys["left"] = False
                if event.key == pygame.K_d:
                    keys["right"] = False
                if event.key == pygame.K_w:
                    keys["up"] = False
                if event.key == pygame.K_s:
                    keys["down"] = False
                if event.key == pygame.K_LSHIFT:  # Отключение ускорения
                    spaceship.is_boosting = False

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()