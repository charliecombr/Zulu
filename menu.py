import pygame
import sys
from config import *
from entities import Car

def show_menu(surface):
    """Exibe o menu inicial do jogo"""
    menu_bg = (0, 0, 40)  # fundo
    title_color = (255, 100, 0)  # título
    option_color = WHITE
    selected_color = (255, 255, 0)  # opção selecionada
    
    options = ["Iniciar Jogo", "Como Jogar", "Sair"]
    selected = 0
    
    font_title = pygame.font.SysFont(None, 80)
    font_options = pygame.font.SysFont(None, 50)
    
    # Carro do menu
    car_img = pygame.Surface((200, 150), pygame.SRCALPHA)
    car = Car()
    car.x = 0
    car.y = 0
    car.draw(car_img)
    
    while True:
        surface.fill(menu_bg)
        
        # Estrada em movimento
        t = pygame.time.get_ticks() / 500
        for i in range(10):
            y = (i * 80 + t * 50) % SCREEN_HEIGHT
            pygame.draw.rect(surface, GRAY, 
                            ((SCREEN_WIDTH - 300) // 2, y, 300, 40))
            
        
        title = font_title.render("CORRIDA", True, title_color)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        
        surface.blit(car_img, (SCREEN_WIDTH // 2 - car_img.get_width() // 2, 220))
        
        for i, option in enumerate(options):
            color = selected_color if i == selected else option_color
            text = font_options.render(option, True, color)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400 + i * 60))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Iniciar Jogo
                        return "start"
                    elif selected == 1:  # Como Jogar
                        show_instructions(surface)
                    elif selected == 2:  # Sair
                        pygame.quit()
                        sys.exit()

def show_instructions(surface):
    """Exibe as instruções do jogo"""
    bg_color = (0, 0, 40)
    text_color = WHITE
    highlight_color = (255, 200, 0)
    
    font_title = pygame.font.SysFont(None, 60)
    font_text = pygame.font.SysFont(None, 30)
    
    instructions = [
        "Como Jogar:",
        "Setas ESQUERDA/DIREITA: Mudar de faixa",
        "Seta CIMA: Acelerar",
        "Seta BAIXO: Frear",
        "ESC: Sair do jogo",
        "Desvie dos outros carros para sobreviver!",
        "Quanto maior sua velocidade, mais pontos você ganha."
    ]
    
    waiting = True
    while waiting:
        surface.fill(bg_color)
        
        title = font_title.render("INSTRUÇÕES", True, highlight_color)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        for i, line in enumerate(instructions):
            color = highlight_color if i == 0 else text_color
            text = font_text.render(line, True, color)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 180 + i * 40))
        
        back_text = font_text.render("Pressione ESPAÇO para voltar", True, highlight_color)
        surface.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 100))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                    waiting = False
                    return