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


def display_card(card_img, x, y):
    Img = pygame.image.load(card_img)
    Img = pygame.transform.scale(Img, (90, 140))
    gameDisplay.blit(Img, (x, y))


def display_named_card(card_name, x, y):
    card_img = card_name + '.png'
    display_card(card_img, x, y)


def display_board(board):
    x = 350
    y = 300
    for card in board:
        display_named_card(card, x, y)
        x += 130


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


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


board = ['diamants', 'chameau', 'épices', 'cuir', 'argent']
player_hand = ['diamants', 'chameau', 'épices', 'cuir', 'argent']

def main_pygame():
    crashed = False
    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        if pygame.mouse.get_pressed()[0] == 1:
            print('CLICKED')
            pygame.draw.rect(gameDisplay, (222, 11, 11), (300, 0, 90, 140))
        pygame.draw.rect(gameDisplay, (222, 11, 11), (400, 0, 90, 140))
        display_camels(0, 0)
        display_board(board)
        display_player_hand(player_hand)
        display_opponent_hand(5)
        pygame.display.update()
        clock.tick(60)

main_pygame()