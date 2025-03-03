import pygame

WHITE = (255, 255, 255)

def draw_score(screen, score):
    font = pygame.font.Font("Romaben-Regular.otf", 36)
    text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(text, (10, 10))
