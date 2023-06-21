import pygame
import sys
import random
import elementos  # Importar la biblioteca adicional
import colores

# Constantes de colores y dimensiones de la ventana
COLOR_CELESTE = (135, 206, 235)
COLOR_VIOLETA = (138, 43, 226)
COLOR_SALMON = (233, 150, 122)
ANCHO_VENTANA = 1920
ALTO_VENTANA = 1080
score = 0

# INCIALIZACION DE PYGAME ----------------------------------------------------------------
pygame.init()

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Intento de Galaxy")

# Imagen de fondo, jugador y laser
imagen_fondo = pygame.image.load("fondo_galaxy.jpg")    
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

imagen_jugador = pygame.image.load("jugador_galaxy.png")
imagen_jugador = pygame.transform.scale(imagen_jugador, (100, 100))

# Laser
imagen_laser = pygame.image.load("jugadorlaser_galaxy.png")
imagen_laser = pygame.transform.scale(imagen_laser, (30, 70))
rect_laser = imagen_laser.get_rect()
# Sonidos laser
sonido_laser = pygame.mixer.Sound("blaster_jugador.mp3")
# Sonidos explosion enemiga
sonido_enemigo = pygame.mixer.Sound("tnt_enemigo.mp3")

# Imagen de Menu de Pausa
imagen_pausa = pygame.image.load("pause.png")
ancho_pausa = ANCHO_VENTANA // 2  # Ajusta el ancho de la imagen
alto_pausa = ALTO_VENTANA // 2  # Ajusta el alto de la imagen
imagen_pausa = pygame.transform.scale(imagen_pausa, (ancho_pausa, alto_pausa))
rect_pausa = imagen_pausa.get_rect()
rect_pausa.centerx = ANCHO_VENTANA // 2
rect_pausa.centery = ALTO_VENTANA // 2

# PONER AL JUGADOR
rect_jugador = imagen_jugador.get_rect()
rect_jugador.centerx = ANCHO_VENTANA // 2
rect_jugador.bottom = ALTO_VENTANA - 10

# Crear lista de enemigos y lasere
lista_enemigos = elementos.crear_lista_enemigos(2, 80, 80)
lista_laser = []

# Bucle principal
flag_correr = True
movimiento_derecha = False  # Bandera para mantener el movimiento hacia la derecha
movimiento_izquierda = False  # Bandera para mantener el movimiento hacia la izquierda


#############################################################################
pausado = False
game_over = False 

fuente = pygame.font.SysFont(None, 36)
nombre = ""

while flag_correr:
    lista_eventos = pygame.event.get()
    tiempo_transcurrido = pygame.time.get_ticks()  # Tiempo que pasa desde que arranca el juego
    TIEMPO_CREACION_PROYECTIL = 300  # 2 segundos (en milisegundos)
    TIEMPO_MOVIMIENTO_NAVES_ENEMIGAS = 360
    
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            # PAUSADO  DEL JUEGO
            if evento.key == pygame.K_UP:
                pausado = not pausado  # Cambiar el estado de pausa al no pausa, osea True
            
            # ABANDONAR EL JUEGO
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
            # Movimiento del jugador
            elif evento.key == pygame.K_LEFT:
                movimiento_izquierda = True
            elif evento.key == pygame.K_RIGHT:
                movimiento_derecha = True

            elif evento.key == pygame.K_DOWN:
                rect_jugador.y += 40

            # Disparo de laser
            elif evento.key == pygame.K_SPACE:    
                sonido_laser.play()
                rect_laser = imagen_laser.get_rect()
                rect_laser.centerx = rect_jugador.x + 50
                rect_laser.bottom = rect_jugador.y 
                lista_laser.append(rect_laser)

        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_RIGHT:
                movimiento_derecha = False
            if evento.key == pygame.K_LEFT:
                movimiento_izquierda = False


#############################################################################

    # Actualizacion de la pantalla
    pantalla.blit(imagen_fondo, (0, 0))
    pantalla.blit(imagen_jugador, rect_jugador)
    pantalla.blit(imagen_laser, rect_laser)

#############################################################################

    ### Actualizacion del movimiento del rect_jugador
    if movimiento_derecha and rect_jugador.right < ANCHO_VENTANA:
        rect_jugador.x += 4
    if movimiento_izquierda and rect_jugador.left > 0:
        rect_jugador.x += -4

    ### Actualizar y dibujar enemigos y LASER JUGADOR
    score = elementos.actualizar_pantalla(lista_enemigos, pantalla, rect_jugador, score, tiempo_transcurrido, TIEMPO_CREACION_PROYECTIL)
    for laser in lista_laser:
        score = elementos.actualizar_pantalla(lista_enemigos, pantalla, laser, score, tiempo_transcurrido, TIEMPO_CREACION_PROYECTIL)
        laser.y -= 7
        pantalla.blit(imagen_laser, laser)

    nuevos_laser = [laser for laser in lista_laser if laser.bottom >= 0] # borra los que estan fuera de pantalla
    lista_laser = nuevos_laser # pasa los lasers a una nueva lista para trabajar con ellos sin borrar los anteriores

    # Mostrar puntuacion
    font = pygame.font.SysFont("Arial", 50)
    texto = font.render("Score: {0}".format(score), True, COLOR_VIOLETA)
    pantalla.blit(texto, (10, 10))
    # Mostrar tiempo
    fontTiempo = pygame.font.SysFont("Arial", 50)
    textoTiempo = fontTiempo.render("Tiempo: {0}".format(round(tiempo_transcurrido/1000)), True, COLOR_VIOLETA)
    pantalla.blit(textoTiempo, (10, 50))

    for enemigo in lista_enemigos:
    # Codigo para actualizar y mover a los enemigos sumado ALEATORIEDAD (como en pokemon)
        if enemigo["direccion"] == "derecha":
            enemigo["rect"].x += enemigo["velocidad"]
            if enemigo["rect"].right >= ANCHO_VENTANA or tiempo_transcurrido % TIEMPO_MOVIMIENTO_NAVES_ENEMIGAS == 0:
                    enemigo["direccion"] = "izquierda"
        else:  # enemigo["direccion"] == "izquierda"
            enemigo["rect"].x -= enemigo["velocidad"]
            if enemigo["rect"].left <= 0 or tiempo_transcurrido % TIEMPO_MOVIMIENTO_NAVES_ENEMIGAS == 0:
                    enemigo["direccion"] = "derecha"


    # Verificacion la pausa
    while pausado: 
        pantalla.blit(imagen_pausa, rect_pausa)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                # Sacar la pausa
                if evento.key == pygame.K_UP:
                    pausado = False
                    break

        pygame.display.flip()

    pygame.display.flip()

