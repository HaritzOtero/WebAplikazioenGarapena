import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Plataformas")

# Colores
WHITE = (255, 255, 255)

# Jugador
player_width = 50
player_height = 50
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height
player_vel = 5
player_jump = -10
player_jump_count = 10
is_jumping = False

# Plataforma
platform_width = 200
platform_height = 20
platform_x = (SCREEN_WIDTH - platform_width) // 2
platform_y = SCREEN_HEIGHT - platform_height - 50

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_vel

    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        if player_jump_count >= -10:
            neg = 1
            if player_jump_count < 0:
                neg = -1
            player_y -= (player_jump_count ** 2) * 0.5 * neg
            player_jump_count -= 1
        else:
            is_jumping = False
            player_jump_count = 10

    # Dibuja la pantalla
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, (0, 255, 0), (platform_x, platform_y, platform_width, platform_height))
    pygame.display.update()

# Salir del juego
pygame.quit()
sys.exit()
