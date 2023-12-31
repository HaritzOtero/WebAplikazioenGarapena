import pygame
import random
import time
import os

# Configuración
pygame.init()
ancho, alto = 640, 480
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Snake Game")
reloj = pygame.time.Clock()

# Colores
negro = (0, 0, 0)
verde = (0, 255, 0)
rojo = (255, 0, 0)
amarillo = (255, 255, 0)
blanco = (255, 255, 255)

# Inicialización de variables
serpiente = [(100, 50), (90, 50), (80, 50)]
serpiente_dir = (10, 0)
comida = (random.randrange(1, ancho // 10) * 10, random.randrange(1, alto // 10) * 10)
fruta_amarilla = None
puntuacion = 0
velocidad = 10  # Velocidad inicial de la serpiente
contador_puntuacion = 0

# Puntuación máxima guardada
puntuacion_maxima = 0

# Directorio donde se guarda la puntuación máxima
directorio_guardado = os.path.dirname(os.path.abspath(__file__))
archivo_puntuacion = os.path.join(directorio_guardado, "puntuacion.txt")

# Tiempo para aparición de la fruta amarilla (10 segundos)
tiempo_aparicion_fruta = 10
tiempo_ultima_aparicion = time.time()

# Fuente de texto
fuente = pygame.font.Font(None, 36)

# Función para dibujar la serpiente y la comida
def dibujar_serpiente(serpiente):
    for segmento in serpiente:
        pygame.draw.rect(pantalla, verde, pygame.Rect(segmento[0], segmento[1], 10, 10))

def dibujar_comida(comida, color):
    pygame.draw.rect(pantalla, color, pygame.Rect(comida[0], comida[1], 10, 10))

def mostrar_puntuacion(puntuacion):
    texto = fuente.render(f"Puntuación: {puntuacion}", True, blanco)
    pantalla.blit(texto, (10, 10))

def mostrar_puntuacion_maxima(puntuacion_maxima):
    texto_maxima = fuente.render(f"Puntuación Máxima: {puntuacion_maxima}", True, blanco)
    x_maxima = ancho - texto_maxima.get_width() - 10  # Posición a la derecha
    pantalla.blit(texto_maxima, (x_maxima, 10))

def guardar_puntuacion_maxima(puntuacion):
    global puntuacion_maxima
    if puntuacion > puntuacion_maxima:
        puntuacion_maxima = puntuacion
        with open(archivo_puntuacion, "w") as archivo:
            archivo.write(str(puntuacion_maxima))

# Función para manejar la aparición de la fruta amarilla
def manejar_fruta_amarilla():
    global fruta_amarilla, tiempo_ultima_aparicion

    # Verificar si ha pasado el tiempo para la aparición de la fruta amarilla
    tiempo_actual = time.time()
    if tiempo_actual - tiempo_ultima_aparicion >= tiempo_aparicion_fruta:
        fruta_amarilla = (random.randrange(1, ancho // 10) * 10, random.randrange(1, alto // 10) * 10)
        tiempo_ultima_aparicion = tiempo_actual

# Cargar la puntuación máxima desde el archivo si existe
if os.path.exists(archivo_puntuacion):
    with open(archivo_puntuacion, "r") as archivo:
        puntuacion_maxima = int(archivo.read())

# Bucle principal del juego
juego_activo = False
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        if not juego_activo:
            # Menú de inicio
            if evento.type == pygame.KEYDOWN:
                juego_activo = True
                serpiente = [(100, 50), (90, 50), (80, 50)]
                serpiente_dir = (10, 0)
                comida = (random.randrange(1, ancho // 10) * 10, random.randrange(1, alto // 10) * 10)
                fruta_amarilla = None
                puntuacion = 0
                contador_puntuacion = 0
                velocidad = 10

        elif juego_activo:
            # Control de la serpiente
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and serpiente_dir != (0, 10):
                    serpiente_dir = (0, -10)
                if evento.key == pygame.K_DOWN and serpiente_dir != (0, -10):
                    serpiente_dir = (0, 10)
                if evento.key == pygame.K_LEFT and serpiente_dir != (10, 0):
                    serpiente_dir = (-10, 0)
                if evento.key == pygame.K_RIGHT and serpiente_dir != (-10, 0):
                    serpiente_dir = (10, 0)

    if juego_activo:
        # Mover la serpiente
        nueva_cabeza = (serpiente[0][0] + serpiente_dir[0], serpiente[0][1] + serpiente_dir[1])
        serpiente.insert(0, nueva_cabeza)

        # Comprobar si la serpiente ha comido la comida
        if serpiente[0] == comida:
            puntuacion += 1
            contador_puntuacion += 1
            comida = (random.randrange(1, ancho // 10) * 10, random.randrange(1, alto // 10) * 10)

            if (puntuacion >= puntuacion_maxima):
                mostrar_puntuacion_maxima(puntuacion)
                
            # Aumentar la velocidad cada 5 puntos
            if contador_puntuacion % 5 == 0:
                velocidad += 1

        # Comprobar si la serpiente ha comido la fruta amarilla
        if fruta_amarilla and serpiente[0] == fruta_amarilla:
            puntuacion += 5
            fruta_amarilla = None

        else:
            serpiente.pop()

        # Comprobar colisiones
        if (
            serpiente[0][0] < 0
            or serpiente[0][0] >= ancho
            or serpiente[0][1] < 0
            or serpiente[0][1] >= alto
            or serpiente[0] in serpiente[1:]
        ):
            juego_activo = False
            guardar_puntuacion_maxima(puntuacion)
            

        # Limpiar pantalla
        pantalla.fill(negro)

        # Dibujar la serpiente, la comida y la fruta amarilla
        dibujar_serpiente(serpiente)
        dibujar_comida(comida, rojo)
        manejar_fruta_amarilla()
        if fruta_amarilla:
            dibujar_comida(fruta_amarilla, amarillo)

        # Mostrar la puntuación
        mostrar_puntuacion(puntuacion)
        mostrar_puntuacion_maxima(puntuacion_maxima)

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        reloj.tick(velocidad)
   # En el bucle principal, ajusta la posición del mensaje del menú de inicio:
    else:
        # Menú de inicio
        pantalla.fill(negro)
        mensaje = fuente.render("Presiona cualquier tecla para empezar", True, blanco)
        x_mensaje = ancho // 2 - mensaje.get_width() // 2
        y_mensaje = alto // 2 - mensaje.get_height() // 2
        pantalla.blit(mensaje, (x_mensaje, y_mensaje))
        mostrar_puntuacion(puntuacion)
        mostrar_puntuacion_maxima(puntuacion_maxima)
        pygame.display.flip()