import pygame, colores, random, sys

COLOR_SALMON = (233, 150, 122)
AQUAMARINE2 = (118, 238, 198)
WHITE = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_BLANCO = (255, 255, 255)

#Incializacion del Pygame y Pymixer
pygame.init()
pygame.mixer.init()
#sonidos explosion enemigas
sonido_enemigo = pygame.mixer.Sound("tnt_enemigo.mp3")
sonido_laser_enemigo = pygame.mixer.Sound("blaster_enemy.mp3")

enemy_imagen_laser = pygame.image.load("enemylaser_galaxy.png")
enemy_imagen_laser = pygame.transform.scale(enemy_imagen_laser, (15, 40))
enemy_imagen_laser = pygame.transform.flip(enemy_imagen_laser, False, True)  # Esto da vuelta la imagen para abajo
rect_laser_enemy = enemy_imagen_laser.get_rect()

imagen_explosion = pygame.image.load("explosion.png")
imagen_explosion = pygame.transform.scale(imagen_explosion, (150, 150))

### IMAGEN DE MUETE
imagen_muerte = pygame.image.load("you_died.jpg")
ancho_muerte = 800  # Ajusta el ancho de la imagen
alto_muerte = 800  # Ajusta el alto de la imagen
imagen_muerte = pygame.transform.scale(imagen_muerte, (ancho_muerte, alto_muerte))
rect_muerte = imagen_muerte.get_rect()
rect_muerte.centerx = 800 // 2
rect_muerte.centery = 800 // 2

ancho_pantalla = 800
alto_pantalla = 600

lista_proyectiles_enemigos = []



lista_proyectiles_enemigos = []

def crear_proyectil_enemigo(lista_enemigos, lista_proyectiles):
    indice_enemigo = random.randrange(len(lista_enemigos))
    enemigo = lista_enemigos[indice_enemigo]
    rect_enemigo = enemigo["rect"]
    x = rect_enemigo.centerx
    y = rect_enemigo.bottom
    proyectil = pygame.Rect(x, y, 30, 70)  # Armar el rectangulo del proyectil
    sonido_laser_enemigo.set_volume(0.1)
    sonido_laser_enemigo.play()
    lista_proyectiles.append(proyectil)


def crear_enemigo(x,y,ancho, alto):  # ESTO ES UN OBJETO? //observacion//
    imagen_enemigo = pygame.image.load("enemy_galaxy.png")
    imagen_enemigo = pygame.transform.scale(imagen_enemigo,(ancho,alto))
    rect_enemigo = imagen_enemigo.get_rect()
    rect_enemigo.x = x
    rect_enemigo.y = y
    #guardar la imagen y el rect en un diccionario
    dic_enemigo = {}
    dic_enemigo["imagen"] = imagen_enemigo
    dic_enemigo["rect"] = rect_enemigo
    dic_enemigo["visible"] = True
    dic_enemigo["direccion"] = "derecha"
    dic_enemigo["velocidad"] = 1
    
    return dic_enemigo

def crear_lista_enemigos(cantidad,anchura,altura):
    lista_enemigos = []
    for i in range(cantidad):
        lista_enemigos.append(crear_enemigo(1100+(i*110),430,anchura,altura))  
        lista_enemigos.append(crear_enemigo(750+(i*90),330,anchura,altura))
        lista_enemigos.append(crear_enemigo(0+(i*90),330,anchura,altura))
        lista_enemigos.append(crear_enemigo(300+(i*130),230,anchura,altura))
        lista_enemigos.append(crear_enemigo(1300+(i*110),130,anchura,altura))    
        lista_enemigos.append(crear_enemigo(10+(i*110),50,anchura,altura))
        lista_enemigos.append(crear_enemigo(800+(i*110),50,anchura,altura))
        lista_enemigos.append(crear_enemigo(1500+(i*130),230,anchura,altura))
        lista_enemigos.append(crear_enemigo(1700+(i*110),130,anchura,altura))  
    return lista_enemigos

def guardar_puntuacion(nombre_jugador, puntuacion):
    with open("ranking.txt", "a") as archivo:
        linea = f"{nombre_jugador},{puntuacion}\n"
        archivo.write(linea)

def pantalla_nombre(score):
    WIDTH = 800
    HEIGHT = 600

    # Crear la ventana
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ingreso de Nombre")

    # Variables para almacenar el nombre
    nombre = ""

    # Bucle principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Cuando se presiona Enter
                    running = False
                elif event.key == pygame.K_BACKSPACE:  # Cuando se presiona Retroceso
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode

        screen.fill((0, 0, 0))  # Limpiar la pantalla
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Ingrese su nombre: " + nombre, True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    print("Nombre ingresado:", nombre)  
    guardar_puntuacion(nombre, score)
    
    pygame.display.flip()
    pygame.time.delay(1000)  # Opcional: Agregar un retraso antes de salir del juego o reiniciarlo
    #sys.exit()

            # POR CONSOLA
# def mostrar_ranking():
#     puntuaciones = []

#     with open("ranking.txt", "r") as archivo:
#         for linea in archivo:
#             # Eliminar espacios en blanco al inicio y al final de la línea
#             linea = linea.strip()

#             # Ignorar las líneas vacías o que no contengan una coma
#             if not linea or "," not in linea:
#                 continue

#             nombre, puntuacion = linea.split(",")
#             puntuaciones.append((nombre, int(puntuacion)))

#     puntuaciones.sort(key=lambda x: x[1], reverse=True)

#     print("RANKING")
#     for i, (nombre, puntuacion) in enumerate(puntuaciones):
#         print(f"{i+1}. {nombre}: {puntuacion}")



def mostrar_ranking():
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)
    imagen_cruz = pygame.image.load("exit.png")
    imagen_cruz = pygame.transform.scale(imagen_cruz, (300, 200))  # Ajustar el tamaño de la imagen si es necesario
    cruz_rect = imagen_cruz.get_rect()
    cruz_rect.x = WIDTH - cruz_rect.width - 5
    cruz_rect.y = 150

    # LEO EL ARCHIVO
    puntuaciones = []
    with open("ranking.txt", "r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or "," not in linea:
                continue
            nombre, puntuacion = linea.split(",")
            puntuaciones.append((nombre, int(puntuacion)))

    # ORDENADO DEL SORT PUNTUACION X[1] Y EL REVERSE DE MAYOR A MENOR 
    puntuaciones.sort(key=lambda x: x[1], reverse=True)

    # CODIGO PARA EL CLICK DEL BOTON DE SALIDA
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cruz_rect.collidepoint(event.pos):
                    running = False

        screen.fill((0, 0, 0))
        y = 100
        # ENUMERACION DE EL TXT
        for i, (nombre, puntuacion) in enumerate(puntuaciones):
            texto = f"{i+1}. {nombre}: {puntuacion}"
            texto_palabras = font.render(texto, True, (255, 255, 255))
            text_rectanguloso = texto_palabras.get_rect(center=(WIDTH // 2, y))
            screen.blit(texto_palabras, text_rectanguloso)
            y += 50

        screen.blit(imagen_cruz, (cruz_rect.x, cruz_rect.y))
        pygame.display.flip() 
    pygame.quit()


game_over = False
def actualizar_pantalla(lista_enemigos, pantalla, rect_jugador, score, TIEMPO_TRANSCURRIDO, TIEMPO_PROYECTIL):
    for e_enemigo in lista_enemigos:
        if e_enemigo["visible"] == True and rect_jugador.colliderect(e_enemigo["rect"]):
            e_enemigo["visible"] = False
            sonido_enemigo.play()
            score = score + 1
            lista_enemigos.remove(e_enemigo)    

        if e_enemigo["visible"] == True:
            pantalla.blit(e_enemigo["imagen"], e_enemigo["rect"])

            if TIEMPO_TRANSCURRIDO % TIEMPO_PROYECTIL == 0 and TIEMPO_TRANSCURRIDO > 0:
                crear_proyectil_enemigo(lista_enemigos, lista_proyectiles_enemigos)
            for proyectil in lista_proyectiles_enemigos:
                proyectil.y += 1
                #     ABANDONAR EL JUEGO CUANDO TE REVIENTAN   //observacion//
                if rect_jugador.colliderect(proyectil): # jugador.superficie y visible=true      
                    game_over = True
                    if game_over:  # if game_over == True
                        pantalla_nombre(score)
                        pygame.time.delay(1000)
                        mostrar_ranking()

                pantalla.blit(enemy_imagen_laser, proyectil)

    return score
