import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

def draw_restart_button(screen):
    font = pygame.font.Font("Romaben-Regular.otf", 28)
    text = font.render("RESTART", True, WHITE)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 25, 120, 50)
    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
    return button_rect

def draw_exit_button(screen):
    font = pygame.font.Font("Romaben-Regular.otf", 28)
    text = font.render("EXIT", True, WHITE)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 25, 70, 50)
    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
    return button_rect
