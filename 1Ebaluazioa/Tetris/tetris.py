import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
GRID = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definición de las piezas de Tetris (cada pieza es una lista de coordenadas)
PIECES = [
    [[1, 1, 1, 1]],            # I-Piece
    [[1, 1], [1, 1]],          # O-Piece
    [[1, 1, 1], [0, 1, 0]],    # T-Piece
    [[1, 1, 1], [1, 0, 0]],    # L-Piece
    [[1, 1, 1], [0, 0, 1]],    # J-Piece
    [[1, 1, 0], [0, 1, 1]],    # S-Piece
    [[0, 1, 1], [1, 1, 0]]     # Z-Piece
]

# Clase para representar una pieza de Tetris
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice([RED, GREEN, BLUE])

    def rotate(self):
        self.shape = list(map(list, zip(*self.shape[::-1])))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def can_move(self, dx, dy):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    if (
                        self.x + i + dx < 0 or
                        self.x + i + dx >= GRID_WIDTH or
                        self.y + j + dy >= GRID_HEIGHT or
                        GRID[self.y + j + dy][self.x + i + dx]
                    ):
                        return False
        return True

    def place(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    GRID[self.y + j][self.x + i] = self.color

    def draw(self, screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, self.color, (self.x * BLOCK_SIZE + i * BLOCK_SIZE, self.y * BLOCK_SIZE + j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, BLACK, (self.x * BLOCK_SIZE + i * BLOCK_SIZE, self.y * BLOCK_SIZE + j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Función para verificar si una fila está completa
def is_row_complete(row):
    return all(cell != 0 for cell in row)

# Función para eliminar filas completas
def remove_complete_rows():
    global GRID
    new_grid = [row for row in GRID if not is_row_complete(row)]
    num_removed_rows = len(GRID) - len(new_grid)
    GRID = [[0 for _ in range(GRID_WIDTH)]] * num_removed_rows + new_grid
    return num_removed_rows

# Función principal del juego
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    current_piece = Piece(GRID_WIDTH // 2 - 1, 0, random.choice(PIECES))
    game_over = False
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_piece.can_move(-1, 0):
                    current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT and current_piece.can_move(1, 0):
                    current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN and current_piece.can_move(0, 1):
                    current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    rotated_piece = current_piece
                    rotated_piece.rotate()
                    if rotated_piece.can_move(0, 0):
                        current_piece = rotated_piece

        if current_piece.can_move(0, 1):
            current_piece.move(0, 1)
        else:
            current_piece.place()
            removed_rows = remove_complete_rows()
            score += removed_rows * 100  # Puntuación por filas completas
            if current_piece.y == 0:
                game_over = True
            else:
                current_piece = Piece(GRID_WIDTH // 2 - 1, 0, random.choice(PIECES))

        screen.fill(BLACK)
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if GRID[y][x]:
                    pygame.draw.rect(screen, GRID[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        current_piece.draw(screen)

        # Mostrar puntuación en la pantalla
        font = pygame.font.Font(None, 36)
        text = font.render(f"Puntuación: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.update()

        clock.tick(2)  # Velocidad de actualización más lenta para hacer el juego más lento

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
