import networkx as nx
import random
import py5
import time

# Tamaño del laberinto
n = 5
jugador_pos = (0, 0)  # Posición inicial del jugador
inicio = (0, 0)
salida = (n - 1, n - 1)

# Generar laberinto como grafo
def generar_laberinto(n):
    G = nx.grid_2d_graph(n, n)
    edges = list(G.edges())
    random.shuffle(edges)
    maze = nx.Graph()
    maze.add_edges_from(edges[:n * n - 1])
    return maze

laberinto = generar_laberinto(n)

# Tiempo límite (en segundos)
tiempo_inicio = time.time()
tiempo_limite = 30

def dibujar_laberinto(grafo):
    py5.stroke(0)  # Color negro para las aristas
    py5.stroke_weight(1)  # Líneas normales
    for (nodo1, nodo2) in grafo.edges():
        x1, y1 = nodo1
        x2, y2 = nodo2
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)


# Dibujar la posición del jugador
def dibujar_jugador(pos):
    x, y = pos
    py5.fill(0, 0, 255)
    py5.ellipse(x * 80 + 40, y * 80 + 40, 20, 20)

# Dibujar la posición de la salida
def dibujar_salida():
    x, y = salida
    py5.fill(0, 255, 0)
    py5.rect(x * 80 + 30, y * 80 + 30, 20, 20)

def dibujar_camino(camino):
    py5.stroke(255, 0, 0)  # Color rojo para el camino
    py5.stroke_weight(3)   # Líneas más gruesas
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)




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

# Configuración inicial de py5
def setup():
    py5.size(400, 400)
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
