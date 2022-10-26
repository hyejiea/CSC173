from random import randint
from tkinter.messagebox import showinfo

from matrix import Matrix
from queue import PriorityQueue
import random
import pygame
import time

BLACK = 0, 0, 0
WHITE = 255,255,255
GRAYBG = 15, 15, 15
BABY_BLUE = 191, 215, 237
BLUE_GROTTO = 96, 163, 217
ROYAL_BLUE = 0, 116, 183
NAVY_BLUE = 0, 59, 115
GREEN = 159, 226, 191
TORQ = 64, 224, 208

WIDTH = 800
HEIGHT = 641
FPS = 60
title = "Sliding Puzzle Game"
TILESIZE = 128
GAME_SIZE = 3

class Puzzle:

    def __init__(self, x, y, width, height, lastSolveTime, move, cost, matrix,  blocks = [], final_state = "1,2,3,4,5,6,7,8,0"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lastSolveTime = lastSolveTime
        self.move = move
        self.cost = cost
        self.matrix = matrix
        self.blocks = blocks
        self.final_state = final_state

    @staticmethod
    def new(x, y, width, height):
        return Puzzle(x, y, width, height, 0, [], 0, Matrix(3,3), [])

    def validNumbers(self, numbers):
        valid = False
        if len(numbers) == 9:
            ref = list(range(9))
            valid = True
            for i in numbers:
                if int(i) not in ref:
                    valid = False
                else: 
                    ref.remove(int(i))
        return valid

    def randomBlocks(self): 
        n = randint(30,40)
        for i in range(n):
            zero = self.matrix.searchBlock(0)
            possibleMoves = []
            #move up
            if zero[0] > 0:
                possibleMoves.append(self.matrix.moveup)
            if zero[0] < 2:
                possibleMoves.append(self.matrix.movedown)
            if zero[1] > 0:
                possibleMoves.append(self.matrix.moveleft)
            if zero[1] < 2:
                possibleMoves.append(self.matrix.moveright)
            random.choice(possibleMoves)(zero)
        self.setBlocksMatrix()

    def setBlocksMatrix(self):
        blocks = []
        block_x=self.x
        block_y=self.y
        block_w = self.width/3
        block_h = self.height/3

        m = self.matrix.getMatrix()
        i=0
        for k in range(3):
            for j in range(3):
                blocks.append({'rect':pygame.Rect(block_x, block_y, block_w, block_h),'color':BABY_BLUE,'block':m[k][j]})
                block_x += block_w+1
                i+=1
            block_y += block_h+1
            block_x = self.x
        self.blocks = blocks

    def setBlocks(self, string):
        numbers = string.split(",")
        blocks = []
        if self.validNumbers(numbers) :
            block_x=self.x
            block_y=self.y

            block_w = self.width/3
            block_h = self.height/3
            self.matrix.buildMatrix(string)
            i=0
            for k in range(3):
                for j in range(3):
                    blocks.append({'rect':pygame.Rect(block_x, block_y, block_w, block_h),'color':BABY_BLUE,'block':int(numbers[i])})
                    block_x += block_w+1 #right
                    i+=1
                block_y += block_h+1 #down
                block_x = self.x
            self.blocks = blocks
            return True
        return False
    


    def initialize(self):
        blocks = self.final_state
        self.setBlocks(blocks)

    def existsIn(self,elem, list = []):
        for item in list:
            if item.isEqual(elem):
                return True
        return False

    def getCost(self,actual):
        while(actual > 0):
            return 1
    

    def bfs(self):

        # breadth-first search function

        inicio = time.time()
        node = self.matrix
        Mfinal = Matrix(3,3)
        Mfinal.buildMatrix(self.final_state) #1,2,3,4,5,6,7,8,0
        final = Mfinal.getMatrix()
        queue = PriorityQueue()
        queue.put(node)
        visitedNodes = []
        n = 1

        while(not node.isEqual(final) and not queue.empty()):
            node = queue.get()
            visitedNodes.append(node)
            moves = []
            childNodes = node.getPossibleNodes(moves)
            for i in range(len(childNodes)):
                if not self.existsIn(childNodes[i].getMatrix(),visitedNodes):
                    childNodes[i].move = moves[i]
                    childNodes[i].manhattanDist()
                    childNodes[i].setPrevious(node)
                    queue._put(childNodes[i])
            n += 1
        moves = []
        self.cost = n
        if(node.isEqual(final)):
            moves.append(node.move)
            nd = node.previous
            while nd != None:
                if nd.move != '':
                    moves.append(nd.move)
                nd = nd.previous
        fim = time.time()
        self.lastSolveTime = fim-inicio
        print("## BFS ##\n")
        print("Time Spent {temp: .5f}:".format(temp = fim-inicio))
        print("You visited:",n,"\n")
        return moves[::-1]

    def a_star(self):
        # starting timer
        inicio = time.time()
        node = self.matrix
        Mfinal = Matrix(3,3)
        Mfinal.buildMatrix(self.final_state) #1,2,3,4,5,6,7,8,0
        final = Mfinal.getMatrix()
        queue = PriorityQueue()
        queue.put(node)
        visitedNodes = []
        indexSelected = 0
        n = 1
        while (not node.isEqual(final) and not queue.empty()):
            node = queue.get()
            visitedNodes.append(node)
            moves = []
            childNodes = node.getPossibleNodes(moves)
            for i in range(len(childNodes)):
                if not self.existsIn(childNodes[i].getMatrix(), visitedNodes):
                    childNodes[i].move = moves[i]
                    childNodes[i].manhattanDist()
                    childNodes[i].setPrevious(node)
                    # Cumulating the cost function
                    childNodes[i].cost = node.cost + node.manhattanDistCost(childNodes[i])
                    childNodes[i].dist += childNodes[i].cost
                    queue._put(childNodes[i])
            n += 1
            auxCost = 0
        moves = []
        self.cost = n
        if(node.isEqual(final)):
            moves.append(node.move)
            nd = node.previous
            while nd != None:
                if nd.move != '':
                    moves.append(nd.move)
                nd = nd.previous

        fim = time.time()
        self.lastSolveTime = fim-inicio
        print("## A* ##\n")
        print("Time spent {temp: .5f}:".format(temp = fim-inicio))
        print("We visited:",n,"\n")

        return moves[::-1]

# class Tile(pygame.sprite.Sprite):

#     def __init__(self, game, x, y, text):
#         self.groups = game.all_sprites
#         pygame.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pygame.Surface((TILESIZE, TILESIZE))
#         self.x, self.y = x, y
#         self.text = text
#         self.rect = self.image.get_rect()
#         if self.text != "empty":
#             # self.font = pygame.font.SysFont("Consolas", 50)
#             # font_surface = self.font.render(self.text, True, BLACK)
#             # self.image.fill(WHITE)
#             self.font_size = self.font.size(self.text)
#             draw_x = (TILESIZE / 2) - self.font_size[0] / 2
#             draw_y = (TILESIZE / 2) - self.font_size[1] / 2
#             self.image.blit((draw_x, draw_y))


#     def update(self):
#         self.rect.x = self.x * TILESIZE
#         self.rect.y = self.y * TILESIZE

#     def click(self, mouse_x, mouse_y):
#         return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

#     def right(self):
#         return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE

#     def left(self):
#         return self.rect.x - TILESIZE >= 0

#     def up(self):
#         return self.rect.y - TILESIZE >= 0

#     def down(self):
#         return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE

class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))
