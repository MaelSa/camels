import socket
from ClientTurn import *
from threading import *
from game import *
from queue import Queue
game = Game()
hote = 'localhost'
port = 8001
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("connecté")
turn = ClientTurn(False)
q = Queue()
q2 = Queue()

def new_recv():
    msg = connexion_avec_serveur.recv(2048).decode()
    dd = 'ok'
    connexion_avec_serveur.send(dd.encode())
    return msg


def new_send(msg):
    connexion_avec_serveur.send(msg.encode())
    ro = connexion_avec_serveur.recv(2048).decode()


import time
from tkinter import *
from tkinter.ttk import *
from functools import partial
import pygame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
activable_buttons = {'échanger': False, 'vendre': False, 'prendre': False, 'chameaux': False}
card_state_board = [False for i in range(5)]
card_state_hand = [False for i in range(5)]
nb_selected_camels = [0, False]
player_name = ['', 0]


def send_tab(tab):
    str = ''
    for t in tab:
        str += t + ','
    str = str[:-1]
    new_send(str)


def receive_tab():
    tab = new_recv()
    return tab.split(',')


def validate(lbl, txt, window):
    player_name[0] = txt.get()
    window.quit()


def first_window():
    window = Tk()
    lbl = Label(window, text="Nom : ")
    lbl.grid(column=0, row=0)
    window.title('LES CAMALS')
    window.geometry('350x200')
    txt = Entry(window, width=10)
    txt.grid(column=1, row=0)
    btn = Button(window, text="Valider", command=partial(validate, lbl, txt, window))
    btn.grid(column=1, row=2)
    window.mainloop()


def display_card(card_img, x, y):

    Img = pygame.image.load(card_img)
    Img = pygame.transform.scale(Img, (90, 140))
    game.display.blit(Img, (x, y))


def display_named_card(card_name, x, y):
    card_img = card_name + '.png'
    display_card(card_img, x, y)


def possible_take_func():
    return len(player_hand) < 5 and card_state_board.count(True) == 1


def possible_camels_func():
    return board.count('chameau') > 0


def possible_sell_func():
    valuable_ressources = ['or', 'diamants', 'argent']
    possible = False
    if card_state_hand.count(True) > 1:
        possible = True
        for i in range(len(player_hand)):
            if card_state_hand[i] == True:
                res = player_hand[i]
        if res in valuable_ressources:
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
        if x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1:
            if card_state_board[i] == True:
                pygame.draw.rect(game.display, (71, 69, 209), (x, y - 5, w + 7, h + 7), 5)
                card_state_board[i] = False
            elif card_state_board[i] == False:
                pygame.draw.rect(game.display, red, (x, y - 5, w + 7, h + 7), 5)
                card_state_board[i] = True
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
                pygame.draw.rect(game.display, (71, 69, 209), (x, y - 5, w + 7, h + 7), 5)
                card_state_hand[i] = False
            elif card_state_hand[i] == False:
                pygame.draw.rect(game.display, red, (x, y - 5, w + 7, h + 7), 5)
                card_state_hand[i] = True
            time.sleep(0.05)
        x += 100


def reset_select():
    card_state_board = [False for i in range(len(board))]
    card_state_hand = [False for i in range(len(player_hand))]
    x = 397
    y = 583
    w = 90
    h = 140
    for i in range(len(player_hand)):
        pygame.draw.rect(game.display, (71, 69, 209), (x, y - 5, w + 7, h + 7), 5)
        x += 100
    x = 347
    y = 303
    w = 90
    h = 140
    for i in range(len(board)):
        pygame.draw.rect(game.display, (71, 69, 209), (x, y - 5, w + 7, h + 7), 5)
        x += 130


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
        pygame.draw.rect(game.display, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game.display, ic, (x, y, w, h))

    smallText = pygame.font.SysFont(None, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    game.display.blit(textSurf, textRect)


def display_score(score):
    pygame.draw.rect(game.display,  (71, 69, 209), (150, 280, 60, 40))
    smallText = pygame.font.SysFont(None, 30)
    textSurf, textRect = text_objects('votre score: '+ str(score), smallText)
    textRect.center = (100, 300)
    game.display.blit(textSurf, textRect)


def disabled_button(msg, x, y, w, h, c):
    pygame.draw.rect(game.display, c, (x, y, w, h))
    smallText = pygame.font.SysFont(None, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    game.display.blit(textSurf, textRect)


def add_selected_camels():
    nb_selected_camels[0] += 1
    smallText = pygame.font.SysFont("comicsansms", 20)
    pygame.draw.rect(game.display, (71, 69, 209), (155, 645, 30, 33))
    textSurf3, textRect3 = text_objects(str(nb_selected_camels[0]), smallText)
    textRect3.center = (170, 650)
    game.display.blit(textSurf3, textRect3)


def pre_add():
    add_selected_camels()


def pre_remove():
    remove_selected_camels()


def remove_selected_camels():
    if nb_selected_camels[0] > 0:
        nb_selected_camels[0] -= 1
        smallText = pygame.font.SysFont("comicsansms", 20)
        pygame.draw.rect(game.display, (71, 69, 209), (160, 645, 30, 33))
        textSurf3, textRect3 = text_objects(str(nb_selected_camels[0]), smallText)
        print(nb_selected_camels)
        textRect3.center = (170, 650)
        game.display.blit(textSurf3, textRect3)


def display_buttons_turn():
    if not q2.empty():
        player_hand = q2.get()
        while not q2.empty():
            q2.get()
        q2.put(player_hand)
        q2.put(player_hand)

    if possible_camels_func():
        button("Chameaux", 1000, 400, 100, 30, white, green, action=take_camels)
    else:
        disabled_button("Chameaux", 1000, 400, 100, 30, grey)
    if possible_trade_func():
        button("Échanger", 1000, 430, 100, 30, white, green, action=trade_cards)
    else:
        disabled_button("Échanger", 1000, 430, 100, 30, grey)
    if possible_take_func():
        button("Prendre", 1000, 460, 100, 30, white, green, action=take_card)
    else:
        disabled_button("Prendre", 1000, 460, 100, 30, grey)
    if possible_sell_func():
        button("Vendre", 1000, 490, 100, 30, white, green, action=sell_ressource)
    else:
        disabled_button("Vendre", 1000, 490, 100, 30, grey)
    button('+', 100, 640, 30, 30, white, green, action=pre_add)
    button('-', 130, 640, 30, 30, white, green, action=pre_remove)


def display_button_not_turn():
    disabled_button("Chameaux", 1000, 400, 100, 30, grey)
    disabled_button("Échanger", 1000, 430, 100, 30, grey)
    disabled_button("Prendre", 1000, 460, 100, 30, grey)
    disabled_button("Vendre", 1000, 490, 100, 30, grey)


def display_camels(player_camels, opponent_camels):
    display_named_card('chameau', 100, 500)
    display_named_card('chameau', 1000, 50)
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf1, textRect1 = text_objects(str(player_camels), smallText)
    textRect1.center = (50, 550)
    game.display.blit(textSurf1, textRect1)
    textSurf2, textRect2 = text_objects(str(opponent_camels), smallText)
    textRect2.center = (1130, 100)
    game.display.blit(textSurf2, textRect2)


def display_player_hand(hand):
    x = 400
    y = 580
    for card in hand:
        display_named_card(card, x, y)
        x += 100


def fill_blank_player_hand(hand):
    if len(hand) < 5:
        x = 800
        y = 580
        """
        for i in range(5 - len(hand)):
            pygame.draw.rect(game.display, (71, 69, 209), (x ,y , 90, 140))
            pygame.draw.rect(game.display, (71, 69, 209), (x, y - 5, 90 + 7, 140 + 7), 5)
            x -= 100
        """
        pygame.draw.rect(game.display, (71, 69, 209), (400, 580, 600, 150))


def display_opponent_hand(c):
    x = 400
    y = 0
    for i in range(c):
        pygame.draw.rect(game.display, (222, 11, 11), (x, y, 90, 140))
        x += 100


def take_card():
    c = 0
    for i in range(len(card_state_board)):

        if card_state_board[i] == True:
            c = i
    new_send('prendre')
    new_send(str(c))
    #if not q2.empty():
    #    player_hand = q2.get()
    board = receive_tab()
    player_hand = receive_tab()
    while not q2.empty():
        q2.get()
    q2.put(player_hand)
    q2.put(player_hand)

    while not q.empty():
        q.get()
    q.put(board)
    q.put(board)
    turn.is_turn = False


def sell_ressource():
    tab_coord = []
    for i in range(len(card_state_hand)):
        if card_state_hand[i] == True:
            c = i
            tab_coord.append(i)
    cb = card_state_hand.count(True)
    res = player_hand[c]
    new_send('vendre')
    new_send(res)
    new_send(str(cb))
    player_hand_rcv = receive_tab()
    while not q2.empty():
        q2.get()
    q2.put(player_hand_rcv)
    fill_blank_player_hand(player_hand_rcv)
    score = int(new_recv())
    display_score(score)
    turn.is_turn = False


def take_camels():
    """
    Func take camels
    :return:
    """
    new_send('chameaux')
    """
    if not q.empty():
        board = q.get()
    for c in board:
        if c == 'chameaux':
            board.remove(c)
    q.put(board)
    """
    board = receive_tab()
    print(f'in camels, we received board : {board}')
    while not q.empty():
        q.get()
    q.put(board)
    q.put(board)
    turn.is_turn = False


def trade_cards():
    '''
    Func to trade cards
    :return:
    '''
    tab_take = []
    tab_give = []
    indexi = []
    new_send('échanger')
    for i in range(len(card_state_hand)):
        if card_state_hand[i] == True:
            tab_give.append(str(i))
    for i in range(len(card_state_board)):
        if card_state_board[i] == True:
            tab_take.append(str(i))

    send_tab(tab_give)
    send_tab(tab_take)
    new_send(str(0))
    board = receive_tab()
    player_hand = receive_tab()
    print(f'we received board : {board} and {player_hand}')
    while not q.empty():
        q.get()
    q.put(board)
    q.put(board)
    while not q2.empty():
        q.get()
    q2.put(player_hand)
    q2.put(player_hand)
    turn.is_turn = False


def main_thread(board, q, q2, player_hand):
    '''
    Thread for pygame func while waiting for the other thread to end
    :return:
    '''
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Jaipur')
    display_width = 1280
    display_height = 720
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    game.display = gameDisplay
    game.display.fill((71, 69, 209))
    display_score(0)

    crashed = False
    cmp = 0
    while not crashed:
        if not q2.empty():
            player_hand = q2.get()
        else:
            q2.put(player_hand)
        if not q.empty():
            board = q.get()
        while not q.empty():
            q.get()
        q.put(board)
        q.put(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        if turn.is_turn:
            display_buttons_turn()
        else:
            display_button_not_turn()
        display_camels(0, 0)
        display_board(board)
        display_player_hand(player_hand)
        display_opponent_hand(5)
        check_clicked_cards_board()
        check_clicked_cards_hand()
        pygame.display.update()
        clock.tick(60)


def side_thread(board, q, q2, player_hand):
    """
    Threads for the player whose not playing, to wait for a signal from the
    server to end the turn
    :return:
    """

    end = False
    while not end:
        if turn.is_turn:
            print('Notre tour')
            board = receive_tab()
            print(f'received board : {board}')
            while not q.empty():
                q.get()
            q.put(board)
            #player_hand = receive_tab()
        end2 = turn.is_turn
        while end2:
            end2 = turn.is_turn
            time.sleep(0.1)
        turn.is_turn = False
        if game.display != None:
            reset_select()
        if not turn.is_turn:
            print('Not our turn')
            s = receive_tab()
            print(f'We received : {s}')
            if s[0] == 'votre':
                turn.is_turn = True
            else:
                board = s
                while not q.empty():
                    q.get()
                q.put(board)
                q.put(board)
            #player_hand = receive_tab()
        while not turn.is_turn:
            s = new_recv()
            print(f'We received : {s}')
            if (s == 'votre'):
                turn.is_turn = True
            else:
                while not q.empty():
                    q.get()
                q.put(board)


first_window()

new_send(player_name[0])
"""
new_send('Ma')
"""
t = new_recv()
if t == '1':
    turn.is_turn = True
else:
    turn.is_turn = False
board = receive_tab()
q.put(board)
player_hand = receive_tab()
q2.put(player_hand)
Thread(target=main_thread, args=(board, q, q2, player_hand)).start()
Thread(target=side_thread, args=(board, q, q2, player_hand)).start()
