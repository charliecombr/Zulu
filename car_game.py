import pygame
import random
import sys

# Inicializar pygame
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

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Configurar a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Carro")
clock = pygame.time.Clock()

class Car:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.lane = 1  # 0: esquerda, 1: meio, 2: direita
        self.speed = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
    
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
    
    def move_right(self):
        if self.lane < 2:
            self.lane += 1
    
    def accelerate(self):
        if self.speed < MAX_SPEED:
            self.speed += SPEED_INCREMENT
    
    def brake(self):
        if self.speed > MIN_SPEED:
            self.speed -= SPEED_DECREMENT
    
    def update(self):
        # Calcular posição x baseada na faixa atual
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        target_x = road_left + (self.lane * LANE_WIDTH) + (LANE_WIDTH - self.width) // 2
        
        # Movimento suave entre faixas
        if self.x < target_x:
            self.x = min(self.x + 10, target_x)
        elif self.x > target_x:
            self.x = max(self.x - 10, target_x)
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    def __init__(self, lane):
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.lane = lane
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        self.x = road_left + (lane * LANE_WIDTH) + (LANE_WIDTH - self.width) // 2
        self.y = -self.height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.passed = False
    
    def update(self, speed):
        self.y += speed
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def draw_road(surface):
    road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
    
    # Desenhar estrada
    pygame.draw.rect(surface, GRAY, (road_left, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    # Desenhar linhas das faixas
    for i in range(1, 3):
        x = road_left + i * LANE_WIDTH
        pygame.draw.line(surface, WHITE, (x, 0), (x, SCREEN_HEIGHT), 3)
    
    # Desenhar bordas da estrada
    pygame.draw.line(surface, WHITE, (road_left, 0), (road_left, SCREEN_HEIGHT), 5)
    pygame.draw.line(surface, WHITE, (road_left + ROAD_WIDTH, 0), (road_left + ROAD_WIDTH, SCREEN_HEIGHT), 5)

def show_game_over(surface, score):
    surface.fill(BLACK)
    font = pygame.font.SysFont(None, 64)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 50))
    
    restart_font = pygame.font.SysFont(None, 36)
    restart_text = restart_font.render("Pressione R para reiniciar", True, GREEN)
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                               SCREEN_HEIGHT // 2 + 120))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Função recursiva para gerar novos obstáculos com base na dificuldade progressiva
def generate_obstacles(obstacles, elapsed_time, last_obstacle_time, obstacle_frequency):
    """
    Função recursiva que decide se deve gerar um novo obstáculo
    com base no tempo decorrido e na frequência atual de obstáculos.
    
    À medida que o jogo avança, a frequência aumenta (tempo entre obstáculos diminui).
    """
    current_time = pygame.time.get_ticks()
    time_since_last = current_time - last_obstacle_time
    
    # Ajustar frequência de obstáculos com base no tempo decorrido
    # Quanto maior o tempo, menor o intervalo entre obstáculos
    adjusted_frequency = max(500, obstacle_frequency - (elapsed_time // 10000) * 100)
    
    if time_since_last > adjusted_frequency:
        # Gerar um novo obstáculo em uma faixa aleatória
        lane = random.randint(0, 2)
        obstacles.append(Obstacle(lane))
        return current_time, adjusted_frequency
    
    return last_obstacle_time, adjusted_frequency

def draw_score(surface, score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (20, 20))

def draw_speed(surface, speed):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Speed: {int(speed*2)} km/h", True, WHITE)
    surface.blit(text, (SCREEN_WIDTH - 180, 20))

def main():
    car = Car()
    obstacles = []
    
    game_over = False
    score = 0
    
    start_time = pygame.time.get_ticks()
    last_obstacle_time = start_time
    obstacle_frequency = 2000  # Inicialmente 2 segundos entre obstáculos
    
    while not game_over:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car.move_left()
                if event.key == pygame.K_RIGHT:
                    car.move_right()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Verificar teclas pressionadas continuamente
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            car.accelerate()
        if keys[pygame.K_DOWN]:
            car.brake()
        
        # Gerar obstáculos usando função recursiva
        last_obstacle_time, obstacle_frequency = generate_obstacles(
            obstacles, elapsed_time, last_obstacle_time, obstacle_frequency
        )
        
        # Atualizar posição do carro
        car.update()
        
        # Atualizar obstáculos e verificar colisões
        for obstacle in obstacles[:]:
            obstacle.update(car.speed)
            
            # Verificar colisão
            if car.get_rect().colliderect(obstacle.get_rect()):
                game_over = True
            
            # Verificar se o obstáculo passou pelo carro sem colidir
            if not obstacle.passed and obstacle.y > car.y + car.height:
                obstacle.passed = True
                score += SCORE_INCREMENT
            
            # Remover obstáculos que saíram da tela
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
        
        # Desenhar elementos
        screen.fill(BLACK)
        draw_road(screen)
        car.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        draw_score(screen, score)
        draw_speed(screen, car.speed)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Exibir tela de fim de jogo
    show_game_over(screen, score)
    main()  # Reiniciar o jogo

if __name__ == "__main__":
    main()