# coding=utf-8
from player import *
from card import *
import random
import socket
from data import *
from threading import *
import time
from queue import Queue
q = Queue()

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(('', 8001))
conn.listen(2)

client1, adress1 = conn.accept()
client2, adress2 = conn.accept()


def new_send(socket_, msg):
    socket_.send(msg.encode())
    b = socket_.recv(2048).decode()


def new_recv(socket_):
    msg = socket_.recv(2048).decode()
    dd = 'ok'
    socket_.send(dd.encode())
    return msg


def shuffle_deck():
    random.shuffle(deck)


def shuffle_bonus():
    for key, value in ressources.items():
        random.shuffle(value)


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def remove_el(liste, el):
    while el in liste:
        liste.remove(el)


def show_line(liste, mess):
    strn = ''
    for l in liste:
        strn += l + ', '
    return mess + strn


def new_buy_ressource_g(player, ressource, nb):
    count = min(nb, len(ressources[ressource]))
    for i in range(count):
        s = ressources[ressource].pop()
        player.add_score(s)
    if len(bonus[count]) >= 1:
        player.add_score(bonus[count].pop())


def end_turn():
    if len(board) < 5:
        for i in range(0, 5-len(board)):
            card = deck.pop()
            board.append(card)


def new_trade_g(player):
    tab_give = receive_tab(player.socket)
    tab_take = receive_tab(player.socket)
    nb_camels_trade = int(new_recv(player.socket))
    for t in tab_give:
        player.hand_str.remove(t)
        board.append(t)
    for t in tab_take:
        player.hand_str.append(t)
        board.remove(t)
    player.nb_camel -= nb_camels_trade
    q.put(board)
    print(board)
    player.is_turn = False


def new_take_camels_g(player):
    nb_camels_on_board = board.count("chameau")
    player.take_camels(nb_camels_on_board)
    for c in range(nb_camels_on_board):
        board.remove('chameau')
    fill_board()
    send_tab(board, player.socket)
    while not q.empty():
        q.get()
    q.put(board)
    player.is_turn = False


def new_turn_g(player):
    board = q.get()
    print('waiting for a choice')
    choice = new_recv(player.socket)
    print(f'choice : {choice}')
    if choice == 'prendre':
        taken_card = new_recv(player.socket)
        player.take_card(taken_card)
        board.remove(taken_card)
        print('success take')
    elif choice == 'vendre':
        res = new_recv(player.socket)
        nb = int(new_recv(player.socket))
        new_buy_ressource_g(player, res, nb)
        print('success buy')
    elif choice == 'chameaux':
        new_take_camels_g(player)
        print('success chameaux')
    elif choice == 'échanger':
        new_trade_g(player)
        print('success trade')
    player.is_turn = False
    q.put(board)

def send_tab(tab, socket):
    str = ''
    for t in tab:
        str += t + ','
    str = str[:-1]
    new_send(socket, str)


def receive_tab(socket):
    tab = new_recv(socket)
    return tab.split(',')


def end_game():
    c = 0
    for key, value in ressources.items():
        if len(value) == 0:
            c += 1
    return c >= 3 or len(deck) == 0


def fill_board():
    if len(board) < 5:
        for i in range(5 - len(board)):
            board.append(deck.pop())


def deal_hand(player):
    for i in range(5):
        player.take_card(deck.pop())
    print(f'La main dealt est {player.hand_str}')
    c = 0
    while c + 1 < len(player.hand_str):
        if player.hand_str[c] == 'chameau':
            player.hand_str.remove('chameau')
            player.nb_camel += 1
        c += 1
    if len(player.hand_str) > 0:
        if player.hand_str[-1] == "chameau":
            player.hand_str.remove("chameau")
            player.nb_camel += 1

    if len(player.hand_str) > 0:
        if player.hand_str[-1] == "chameau":
            player.hand_str.remove("chameau")
            player.nb_camel += 1

    if len(player.hand_str) > 0:
        if player.hand_str[-1] == "chameau":
            player.hand_str.remove("chameau")
            player.nb_camel += 1

    if len(player.hand_str) > 0:
        if player.hand_str[-1] == "chameau":
            player.hand_str.remove("chameau")
            player.nb_camel += 1

    if len(player.hand_str) > 0:
        if player.hand_str[-1] == "chameau":
            player.hand_str.remove("chameau")
            player.nb_camel += 1


def setup_game():
    shuffle_deck()
    shuffle_bonus()
    fill_board()


def main_thread(player, q):
    board = q.get()
    send_tab(board, player.socket)
    send_tab(player.hand_str, player.socket)
    q.put(board)
    while not end_game():
        board = q.get()
        send_tab(board, player.socket)
        #send_tab(player.hand_str, player.socket)
        if player.is_turn:
            # new_send(player.socket, str(player.nb_camel))
            q.put(board)
            new_turn_g(player)
            player.is_turn = False
            player.other_player.is_turn = True
            fill_board()
            board = q.get()
            q.put(board)
        while not player.is_turn:
            time.sleep(0.1)
        new_send(player.socket, 'votre')
        player.is_turn = True
        player.other_player.turn = False



def new_game():
    name1 = new_recv(client1)
    print(f'Premier joueur : {name1}')
    name2 = new_recv(client2)
    print(f'Second joueur : {name2}')
    joueur1 = Player(name1, client1, client2, 1)
    joueur2 = Player(name2, client2, client1, 2)
    joueur1.other_player = joueur2
    joueur2.other_player = joueur1
    joueur1.nb_camel = 0
    joueur2.nb_camel = 0
    setup_game()
    deal_hand(joueur1)
    deal_hand(joueur2)
    q.put(board)
    q.put(board)
    joueur1.is_turn = True
    joueur2.is_turn = False
    new_send(joueur1.socket, '1')
    new_send(joueur2.socket, '2')

    Thread(target=main_thread, args=(joueur2, q)).start()
    Thread(target=main_thread, args=(joueur1, q)).start()


new_game()
