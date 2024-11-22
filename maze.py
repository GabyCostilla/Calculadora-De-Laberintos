import networkx as nx
import random
import py5
import time

# Variable global para la dificultad seleccionada
dificultad = 5  # 1 = fácil, 2 = media, 3 = difícil

# Tamaño del laberinto según la dificultad
def obtener_tamano_laberinto(dificultad):
    if dificultad == 1:
        return 5  # Fácil
    elif dificultad == 2:
        return 10  # Media
    else:
        return 15  # Difícil

# Posición del jugador y la salida
jugador_pos = (0, 0)  # Posición inicial del jugador
inicio = (0, 0)
salida = None

# Generar laberinto como grafo
def generar_laberinto(n):
    G = nx.grid_2d_graph(n, n)
    edges = list(G.edges())
    random.shuffle(edges)
    maze = nx.Graph()
    maze.add_edges_from(edges[:n * n - 1])
    return maze

# Establecer tamaño y generar laberinto con dificultad seleccionada
n = obtener_tamano_laberinto(dificultad)
salida = (n - 1, n - 1)
laberinto = generar_laberinto(n)

# Tiempo límite (en segundos)
tiempo_inicio = time.time()
tiempo_limite = 30

# Ajustar la escala de dibujo en función del tamaño del laberinto
tamaño_celda = 500 // n  # 400px de ancho / n filas (se ajusta según la dificultad)

def dibujar_laberinto(grafo):
    py5.no_fill()
    py5.stroke_weight(2)  # Grosor de las líneas de las paredes
    
    # Definir los colores de las paredes y las aristas
    py5.stroke(0, 0, 0)  # Color negro para las paredes
    py5.stroke_weight(3)  # Paredes más gruesas para mayor visibilidad
    
    # Dibujar las paredes
    for (nodo1, nodo2) in grafo.edges():
        x1, y1 = nodo1
        x2, y2 = nodo2
        py5.line(x1 * tamaño_celda + 40, y1 * tamaño_celda + 40, x2 * tamaño_celda + 40, y2 * tamaño_celda + 40)

def dibujar_jugador(pos):
    x, y = pos
    py5.fill(0, 121, 255)  # Color azul para el jugador
    
    # Añadir bordes suaves a la forma del jugador
    py5.no_stroke()
    py5.ellipse(x * tamaño_celda + 40, y * tamaño_celda + 40, 24, 24)
    
    # Agregar un brillo alrededor del jugador para destacar
    py5.fill(255, 255, 255, 100)  # Color blanco semitransparente para el brillo
    py5.ellipse(x * tamaño_celda + 40, y * tamaño_celda + 40, 32, 32)  # Brillo suave

# Dibujar la posición de la salida
def dibujar_salida():
    x, y = salida
    py5.fill(0, 255, 0)
    py5.rect(x * tamaño_celda + 30, y * tamaño_celda + 30, 20, 20)

def dibujar_camino(camino):
    py5.stroke(255, 0, 0)  # Color rojo para el camino
    py5.stroke_weight(3)   # Líneas más gruesas
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        py5.line(x1 * tamaño_celda + 40, y1 * tamaño_celda + 40, x2 * tamaño_celda + 40, y2 * tamaño_celda + 40)

def encontrar_camino_dfs(grafo, inicio, objetivo, visitados=None):
    if visitados is None:
        visitados = set()

    # Agregar el nodo inicial a los visitados
    visitados.add(inicio)

    # Si encontramos el objetivo, devolvemos el camino
    if inicio == objetivo:
        return [inicio]

    # Explorar cada vecino del nodo actual
    for vecino in grafo.neighbors(inicio):
        if vecino not in visitados:  # Solo explorar nodos no visitados
            camino = encontrar_camino_dfs(grafo, vecino, objetivo, visitados)
            if camino:  # Si encontramos un camino válido
                return [inicio] + camino

    return None  # No hay camino desde este nodo

def mostrar_solucion():
    # Calcular el camino desde el jugador a la salida
    camino = encontrar_camino_dfs(laberinto, jugador_pos, salida)

    if not camino:
        print("No se encontró un camino desde la posición actual a la salida")
        return

    print(f"Camino encontrado desde {jugador_pos} hasta {salida}: {camino}")
    dibujar_camino(camino)

# Mostrar el tiempo restante en pantalla
def mostrar_tiempo_restante():
    tiempo_actual = time.time()
    tiempo_restante = max(0, tiempo_limite - int(tiempo_actual - tiempo_inicio))
    py5.fill(0)
    py5.text_size(20)
    py5.text(f"Tiempo restante: {tiempo_restante}s", 10, 30)

def setup():
    py5.size(800, 800)  # Aumentar el tamaño de la ventana a 800x800
    py5.background(255)


def draw():
    global jugador_pos
    py5.background(255)  # Limpia la pantalla

    # Dibujar el laberinto y el jugador
    dibujar_laberinto(laberinto)
    dibujar_jugador(jugador_pos)
    dibujar_salida()

    # Mostrar el tiempo restante
    mostrar_tiempo_restante()

    # Verificar si se acabó el tiempo
    tiempo_actual = time.time()
    if tiempo_actual - tiempo_inicio > tiempo_limite:
        mostrar_solucion()

def key_pressed():
    global jugador_pos
    x, y = jugador_pos

    # Asegurarse de que los nodos están dentro del grafo
    if (x, y) not in laberinto.nodes():
        print(f"El nodo {jugador_pos} no está en el grafo. Reintentando...")
        return

    if py5.key == py5.CODED:
        if py5.key_code == py5.UP and (x, y - 1) in laberinto.neighbors((x, y)):
            jugador_pos = (x, y - 1)
        elif py5.key_code == py5.DOWN and (x, y + 1) in laberinto.neighbors((x, y)):
            jugador_pos = (x, y + 1)
        elif py5.key_code == py5.LEFT and (x - 1, y) in laberinto.neighbors((x, y)):
            jugador_pos = (x - 1, y)
        elif py5.key_code == py5.RIGHT and (x + 1, y) in laberinto.neighbors((x, y)):
            jugador_pos = (x + 1, y)

        # Verificar si el jugador ha llegado a la salida
        if jugador_pos == salida:
            py5.no_loop()  # Detener el juego
            print("¡Felicidades! Has llegado a la salida.")

# Ejecutar el sketch
py5.run_sketch()
