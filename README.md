# Proyecto: Laberinto Interactivo

Este proyecto consiste en la creación de un laberinto interactivo en 2D utilizando Python y la librería `py5` para la visualización gráfica. El laberinto se genera dinámicamente y permite que el jugador se mueva dentro del laberinto mientras sigue una serie de reglas.

## Características

- **Generación de laberinto**: El laberinto se genera como un grafo, donde cada celda es un nodo y las conexiones entre celdas son aristas.
- **Visualización**: Se dibujan las paredes del laberinto y el jugador, que puede moverse dentro del mismo.
- **Interactividad**: El jugador puede moverse con las teclas de flecha. El objetivo es encontrar la salida del laberinto.

## Funciones Principales

### `dibujar_laberinto(grafo)`

Dibuja el laberinto en pantalla utilizando el objeto `grafo`, que representa el laberinto. La función recorre las aristas del grafo y dibuja las líneas entre las celdas conectadas.

#### Detalles de la implementación:

- **Grosor de las líneas**: Se usa un grosor de línea de 3 para hacer las paredes más visibles.
- **Color**: El color de las paredes del laberinto es negro (`py5.stroke(0, 0, 0)`).

### `dibujar_jugador(pos)`

Dibuja al jugador en su posición actual dentro del laberinto. El jugador se representa como un círculo azul, con un resplandor suave a su alrededor para hacerlo más visible.

#### Detalles de la implementación:

- **Color del jugador**: Azul (`py5.fill(0, 121, 255)`).
- **Tamaño**: El jugador es un círculo de 24 píxeles de diámetro.
- **Brillo**: Un resplandor blanco y semitransparente (con opacidad del 100) rodea al jugador, destacándolo visualmente.

## Requisitos

Para ejecutar este proyecto, necesitas tener Python instalado en tu máquina y las siguientes librerías:

- `py5`: Librería para crear gráficos interactivos en Python.
- `networkx`: Librería para la manipulación de grafos en Python.

### Instalación de dependencias

Para instalar las dependencias necesarias, puedes ejecutar:

```bash
pip install py5 networkx
