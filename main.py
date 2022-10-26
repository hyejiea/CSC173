from turtle import color
from puzzle import Puzzle
import pygame
import pygame_gui
import time
# import constant
import os

SCREEN_SIZE = (1000, 720)
BLACK = 0, 0, 0
WHITE = 255,255,255
GRAYBG = 15, 15, 15
BABY_BLUE = 191, 215, 237
BLUE_GROTTO = 96, 163, 217
ROYAL_BLUE = 0, 116, 183
NAVY_BLUE = 0, 59, 115
GREEN = 159, 226, 191
TORQ = 64, 224, 208


pygame.init()
BASICFONT = pygame.font.SysFont('FiraCode-Retina.ttf',50)

pygame.display.set_caption('8 Puzzle')
window_surface = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(SCREEN_SIZE)
background.fill(pygame.Color(WHITE))
manager = pygame_gui.UIManager(SCREEN_SIZE)

programIcon = pygame.image.load(os.path.abspath("C:/Users/User/Desktop/eight_puzzle_Final/8_puzzle/logo.png"))
pygame.display.set_icon(programIcon)

pygame_gui.core.IWindowInterface.set_display_title(self=window_surface,new_title="8 Puzzle")

def display_elements():
    #Elements
    ### Title Label
    pygame_gui.elements.ui_label.UILabel(manager=manager,
                                        text="8 Puzzle Game",
                                        relative_rect=pygame.Rect((350, 10), (300, 70)),
                                        object_id="#title_box"
                                        )

display_elements()
### solve button
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 420), (250, 30)),
                                             text='Solve Puzzle',
                                             manager=manager,
                                             object_id="#solve_btn")

### algorithmOptions DropDown
dropdown_layout_rect = pygame.Rect((650, 380), (250, 30))
algorithmOptions = ["A* (Manhatan Distance)","BFS (Manhatan Distance)"]
algorithmDropDown = pygame_gui.elements.UIDropDownMenu(options_list=algorithmOptions,
                                                       starting_option=algorithmOptions[1],
                                                       relative_rect=dropdown_layout_rect,
                                                       manager=manager)

### Search label
pygame_gui.elements.ui_label.UILabel(parent_element=algorithmDropDown,
                                     manager=manager,
                                     text="Heuristic Search:", # (pos-width,pos-height),(width,height)
                                     relative_rect=pygame.Rect((650, 350), (250, 30)))
### shuffle button
button_layout_rect = pygame.Rect((650, 300), (250, 30))
shuffle_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='Shuffle',
                                             manager=manager)
### alert label
alert_label = pygame_gui.elements.ui_label.UILabel(
                                     manager=manager,
                                     text="",
                                     relative_rect=pygame.Rect((920, 320), (250, 30)),
                                     object_id="#accept_label")

def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface,BLUE_GROTTO, block['rect'])
            textSurf = BASICFONT.render(str(block['block']), True,WHITE)
            textRect = textSurf.get_rect()
            textRect.center = block['rect'].left+50,block['rect'].top+50
            window_surface.blit(textSurf, textRect)
        else:
            pygame.draw.rect(window_surface,ROYAL_BLUE, block['rect'])

def solveAnimation(moves):
    for mv in moves:
        zero = puzzle.matrix.searchBlock(0)
        if mv == "right":
            puzzle.matrix.moveright(zero)
        elif mv == "left":
            puzzle.matrix.moveleft(zero)  
        elif mv == "up":
            puzzle.matrix.moveup(zero)
        elif mv == "down":
            puzzle.matrix.movedown(zero)
        puzzle.setBlocksMatrix()
        draw_blocks(puzzle.blocks)
        pygame.display.update()
        time.sleep(0.2)

window_surface.blit(background, (0, 0))
pygame.display.update()
clock = pygame.time.Clock()
puzzle = Puzzle.new(250, 220, 330, 330)
puzzle.initialize()
algorithm = "BFS (Manhatan Distance)"
fstate="1,2,3,4,5,6,7,8,0"
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    puzzle.randomBlocks()

                elif event.ui_element == solve_button:

                    if algorithm == "BFS (Manhatan Distance)":
                        moves = puzzle.bfs()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                        # Confirmation Box - Algorithm Report
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                )
                        solveAnimation(moves)

                    elif algorithm == "A* (Manhatan Distance)":
                        moves = puzzle.a_star()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                        # Confirmation Box - Algorithm Report
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                )
                        solveAnimation(moves)

            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithmDropDown:
                    algorithm = event.text
        manager.process_events(event)

    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    draw_blocks(puzzle.blocks)
    pygame.display.update()
