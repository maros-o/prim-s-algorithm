import pygame
import random
import os

pygame.font.init()

X, Y = 38, 24
HALF_X = X//2
HALF_Y = Y//2
BLOCK_SIZE = 32
WIDTH, HEIGHT = X * BLOCK_SIZE, Y * BLOCK_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont('consolas', 20)

BGCOLOR = (130, 200, 255)
TEXTCOLOR = (255, 255, 255)
NODECOLOR = (210, 105, 30)
GRIDCOLOR = (150, 220, 255)

class Node():
    def __init__(self, pos, number):
        self.pos = pos
        self.number = number

    def get_pos(self):
        return self.pos

    def get_number(self):
        return self.number  

def draw_grid():
    for x in range(1, X):
        pygame.draw.line(WIN, GRIDCOLOR, [x * BLOCK_SIZE, 0], [x * BLOCK_SIZE, Y * BLOCK_SIZE])
    for y in range(1, Y):
        pygame.draw.line(WIN, GRIDCOLOR, [0, y * BLOCK_SIZE], [X * BLOCK_SIZE, y * BLOCK_SIZE])

def draw_window(nodes, edges):
    WIN.fill(BGCOLOR)

    draw_grid()
    draw_nodes(nodes)
    draw_edges(nodes, edges)
    draw_nodes(nodes)

    pygame.display.update()

def draw_edges(nodes, edges):
    for edge in edges:
        for pos_x in range(0, HALF_X):
            for pos_y in range(0, HALF_Y):
                if (nodes[pos_x][pos_y].get_number() == edge[0][0]):
                    start = nodes[pos_x][pos_y].get_pos()
                if (nodes[pos_x][pos_y].get_number() == edge[0][1]):
                    end = nodes[pos_x][pos_y].get_pos()

        weight = edge[1]
        weight_color_power = 60

        color = (180 - weight * weight_color_power, 180 - weight * weight_color_power, 180 - weight * weight_color_power)

        pygame.draw.line(WIN, color, [start[0] * BLOCK_SIZE, start[1] * BLOCK_SIZE], [end[0] * BLOCK_SIZE, end[1] * BLOCK_SIZE ], 4 + weight * 4)
        pygame.display.update()

def draw_nodes(nodes):
    for x in range(0, HALF_X):
        for y in range(0, HALF_Y):
            pos_x, pos_y = nodes[x][y].get_pos()
            number = nodes[x][y].get_number()

            circle_radius = 18
            pygame.draw.circle(WIN, NODECOLOR, [pos_x * BLOCK_SIZE, pos_y * BLOCK_SIZE], circle_radius)

            text = FONT.render(str(number), 1, TEXTCOLOR)
            WIN.blit(text, (pos_x * BLOCK_SIZE - text.get_rect().width // 2, pos_y * BLOCK_SIZE - text.get_rect().height // 2))
            pygame.display.update()

def create_nodes():
    nodes = [[Node((x*2+1, y*2+1), x + y * HALF_X) for y in range(0, HALF_Y)] for x in range(0, HALF_X)]
    return nodes

def create_edges():
    edges = [[0 for y in range(0, HALF_Y * HALF_X)] for x in range(0, HALF_X * HALF_Y)]

    skiplist = [HALF_X * x for x in range(0, HALF_X)]
    for x in range(0, HALF_X * HALF_Y):
        for y in range(0, HALF_Y * HALF_X):
            if not (x == y):
                if (x + 1 == y and y not in skiplist): edges[x][y] = random.randint(1, 3)
                elif (x + HALF_X == y): edges[x][y] = random.randint(1, 3)

    return edges

def prims_algoritm(edges):
    clean_edges = []
    for x in range(0, HALF_X * HALF_Y):
        for y in range(0, HALF_Y * HALF_X):
            if not (edges[x][y] == 0):
                clean_edges.append(((x, y), edges[x][y]))
            
    visited = []
    unvisited = [x for x in range(HALF_X * HALF_Y)]
    curr = 0

    final_edges = []
    while len(unvisited) > 0:
        visited.append(curr)

        for number in unvisited:
            if number in visited:
                unvisited.remove(number)

        my_edges = []
        for edge in clean_edges:
            if ((edge[0][0] in visited or edge[0][1] in visited) and not (edge[0][0] in visited and edge[0][1] in visited)):
                my_edges.append(edge)

        min_edge = ((-1, -1), 999)

        for edge in my_edges:
            if (edge[1] < min_edge[1]):
                min_edge = edge
        
        if len(unvisited) == 0:
            break

        final_edges.append(min_edge)

        if min_edge[0][0] == -1:
            curr = unvisited[0]
        else:
            if (min_edge[0][1] in visited):
                curr = min_edge[0][0]
            else:
                curr = min_edge[0][1]

    return final_edges

def main():
    pygame.display.set_caption("prim's algoritm")

    nodes = create_nodes()
    edges = create_edges()

    final_edges = prims_algoritm(edges)

    draw_window(nodes, final_edges)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main()
