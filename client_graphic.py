import socket
"""
hote = 'localhost'
port = 8001
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("connecté")
def new_recv():
    msg = connexion_avec_serveur.recv(2048).decode()
    dd = 'ok'
    connexion_avec_serveur.send(dd.encode())
    return msg


def new_send(msg):
    connexion_avec_serveur.send(msg.encode())
    ro = connexion_avec_serveur.recv(2048).decode()
"""
import time
from tkinter import *
from tkinter.ttk import *
from functools import partial
import pygame

board = ['diamants', 'chameau', 'épices', 'cuir', 'argent']
player_hand = ['diamants', 'chameau', 'épices', 'cuir', 'argent']
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
activable_buttons = {'échanger': False, 'vendre': False, 'prendre': False, 'chameaux': False}

def validate(lbl, txt, window):
    print(txt.get())
    window.quit()


def first_window():
    window = Tk()
    lbl = Label(window, text="Nom : ")
    lbl.grid(column=0, row=0)
    window.title('LES CAMALS')
    txt = Entry(window, width=10)
    txt.grid(column=1, row=0)
    btn = Button(window, text="Valider", command=partial(validate, lbl, txt, window))
    btn.grid(column=1, row=2)

    window.mainloop()

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Jaipur')
display_width = 1280
display_height = 720
gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill((71, 69, 209))


card_state_board = [False for i in range(5)]
card_state_hand = [False for i in range(5)]
nb_selected_camels = [0, False]


def display_card(card_img, x, y):
    Img = pygame.image.load(card_img)
    Img = pygame.transform.scale(Img, (90, 140))
    gameDisplay.blit(Img, (x, y))


def display_named_card(card_name, x, y):
    card_img = card_name + '.png'
    display_card(card_img, x, y)


def possible_take_func():
    return len(player_hand) < 5 and card_state_board.count(True) == 1


def possible_camels_func():
    return board.count('chameau') > 0


def possible_sell_func():
    possible = False
    if card_state_hand.count(True) > 1:
        possible = True
        for i in range(len(player_hand)):
            if card_state_hand[i] == True:
                res = player_hand[i]
        for i in range(len(player_hand)):
            if card_state_hand[i] == True and player_hand[i] != res:
                possible = False
    return possible


def possible_trade_func():

    tot_from_player = nb_selected_camels[0] + card_state_hand.count(True)
    return tot_from_player == card_state_board.count(True) and tot_from_player > 1 and (len(player_hand) + nb_selected_camels[0] < 6)


def check_clicked_cards_board():
    x = 347
    y = 303
    w = 90
    h = 140
    for i in range(len(board)):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1 and board[i] != 'chameau':
            if card_state_board[i] == True:
                pygame.draw.rect(gameDisplay, (71, 69, 209), (x, y - 5, w + 7, h + 7), 5)
                card_state_board[i] = False
                print('there')
            elif card_state_board[i] == False:
                pygame.draw.rect(gameDisplay, red, (x, y - 5, w + 7, h + 7), 5)
                card_state_board[i] = True
                print('here')
            time.sleep(0.05)
        x += 130


def check_clicked_cards_hand():
    x = 397
    y = 583
    w = 90
    h = 140
    for i in range(len(player_hand)):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1:
            if card_state_hand[i] == True:
                pygame.draw.rect(gameDisplay, (71, 69, 209), (x, y - 5, w + 7, h + 7), 5)
                card_state_hand[i] = False
                print('there')
            elif card_state_hand[i] == False:
                pygame.draw.rect(gameDisplay, red, (x, y - 5, w + 7, h + 7), 5)
                card_state_hand[i] = True
                print('here')
            time.sleep(0.05)
        x += 100


def display_board(board):
    x = 350
    y = 300
    for card in board:
        display_named_card(card, x, y)
        x += 130


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            print('ON EXE ICI ')
            action()
            print("something is happening")
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont(None, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)


def disabled_button(msg, x, y, w, h, c):
    pygame.draw.rect(gameDisplay, c, (x, y, w, h))
    smallText = pygame.font.SysFont(None, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def add_selected_camels():
    nb_selected_camels[0] += 1
    print("exe+")
    smallText = pygame.font.SysFont("comicsansms", 20)
    pygame.draw.rect(gameDisplay, (71, 69, 209), (155, 645, 30, 33))
    textSurf3, textRect3 = text_objects(str(nb_selected_camels[0]), smallText)
    print(nb_selected_camels)
    textRect3.center = (170, 650)
    gameDisplay.blit(textSurf3, textRect3)


def pre_add():
    add_selected_camels()


def pre_remove():
    remove_selected_camels()


def remove_selected_camels():
    if nb_selected_camels[0] > 0:
        nb_selected_camels[0] -= 1
        print("exe-")
        smallText = pygame.font.SysFont("comicsansms", 20)
        pygame.draw.rect(gameDisplay, (71, 69, 209), (160, 645, 30, 33))
        textSurf3, textRect3 = text_objects(str(nb_selected_camels[0]), smallText)
        print(nb_selected_camels)
        textRect3.center = (170, 650)
        gameDisplay.blit(textSurf3, textRect3)


def display_buttons_turn():
    if possible_camels_func():
        button("Chameaux", 1000, 400, 100, 30, white, green)
    else:
        disabled_button("Chameaux", 1000, 400, 100, 30, grey)
    if possible_trade_func():
        button("Échanger", 1000, 430, 100, 30, white, green)
    else:
        disabled_button("Échanger", 1000, 430, 100, 30, grey)
    if possible_take_func():
        button("Prendre", 1000, 460, 100, 30, white, grey)
    else:
        disabled_button("Prendre", 1000, 460, 100, 30, grey)
    if possible_sell_func():
        button("Vendre", 1000, 490, 100, 30, white, green)
    else:
        disabled_button("Vendre", 1000, 490, 100, 30, grey)
    button('+', 100, 640, 30, 30, white, green, action=pre_add)
    button('-', 130, 640, 30, 30, white, green, action=pre_remove)


def display_camels(player_camels, opponent_camels):
    display_named_card('chameau', 100, 500)
    display_named_card('chameau', 1000, 50)
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf1, textRect1 = text_objects(str(player_camels), smallText)
    textRect1.center = (50, 550)
    gameDisplay.blit(textSurf1, textRect1)
    textSurf2, textRect2 = text_objects(str(opponent_camels), smallText)
    textRect2.center = (1130, 100)
    gameDisplay.blit(textSurf2, textRect2)

    display_buttons_turn()


def display_player_hand(hand):
    x = 400
    y = 580
    for card in hand:
        display_named_card(card, x, y)
        x += 100


def display_opponent_hand(c):
    x = 400
    y = 0
    for i in range(c):
        pygame.draw.rect(gameDisplay, (222, 11, 11), (x, y, 90, 140))
        x += 100




def main_pygame():
    crashed = False
    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        pygame.draw.rect(gameDisplay, (222, 11, 11), (400, 0, 90, 140))
        display_camels(0, 0)
        display_board(board)
        display_player_hand(player_hand)
        display_opponent_hand(5)
        check_clicked_cards_board()
        check_clicked_cards_hand()
        pygame.display.update()
        clock.tick(60)

main_pygame()