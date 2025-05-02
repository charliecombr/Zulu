import pygame

pygame.init()

# Configurações do jogo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROAD_WIDTH = 400
LANE_WIDTH = ROAD_WIDTH // 3
CAR_WIDTH = 50
CAR_HEIGHT = 100
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
SPEED_INCREMENT = 0.5
SPEED_DECREMENT = 0.3
MIN_SPEED = 3
MAX_SPEED = 15
SCORE_INCREMENT = 5

MAX_PARTICLES = 50

DAY_CYCLE_DURATION = 60000  # 60 segundos
SKY_COLORS = [
    (135, 206, 235),  # Azul claro (meio-dia)
    (255, 200, 100),  # Laranja (pôr do sol)
    (50, 50, 100),    # Azul escuro (noite)
    (100, 120, 150)   # Azul acinzentado (amanhecer)
]
CLOUD_COLORS = [
    (255, 255, 255),  # Branco (dia)
    (255, 200, 150),  # Laranja claro (pôr do sol)
    (100, 100, 120),  # Cinza escuro (noite)
    (200, 200, 220)   # Cinza claro (amanhecer)
]
MAX_CLOUDS = 7

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Carro")
clock = pygame.time.Clock()