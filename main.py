# coding=utf-8
from player import *
from card import *
import random
import socket
from data import *


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(('', 8000))
conn.listen(5)

client1, adress1 = conn.accept()
client2, adress2 = conn.accept()

def shuffle_deck():
    random.shuffle(deck)


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def remove_el(list, el):
        while el in list:
            list.remove(el)


def show_line(list, mess):
    str = ''
    for l in list:
        str += l + ', '
    return mess, str


def trade_1(player):
    ok_pre_trade = False
    nb_camels_trade = 0
    nb_cards_trade = 0
    while not ok_pre_trade:
        ok_camels = False
        while not ok_camels:
            nb_camels_trade = player.socket.recv(2048).decode()
            if 0 <= nb_camels_trade <= min(player.nb_camel, 5-len(player.hand_str)):
                ok_camels = True
                player.socket.send('true'.encode())
            else:
                print("Nombre de chameaux non valide")
                player.socket.send('false'.encode())
        ok_cards = False
        while not ok_cards:
            nb_cards_trade = player.socket.recv(2048).decode()
            if 0<= nb_cards_trade <= len(player.hand_str):
                ok_cards = True
                player.socket.send('true'.encode())
            else:
                print("Nombre de cartes non valide")
                player.socket.send('false'.encode())
        total_trade = nb_camels_trade + nb_cards_trade
        if 2 <= total_trade <= (5 - board.count("chameau")):
            ok_pre_trade = True
            player.socket.send('true'.encode())
        else:
            print("Les données de l'échange ne sont pas valides")
            player.socket.send('false'.encode())
    ok_choice_cards = False
    chosen_cards = []
    while not ok_choice_cards:
        chosen_cards = []
        possible_choices = player.hand_str
        for i in range(0, nb_cards_trade):
            player.socket.send(show_line(possible_choices, 'Choix possibles : ').encode())
            player.socket.send(show_line(chosen_cards, 'Cartes choisies : ').enccode())
            ok_choice_c = False
            choice = ''
            while not ok_choice_c:
                player.socket.send('Choix ?'.encode())
                choice = player.socket.recv(2048).decode()
                ok_choice_c = (choice in possible_choices)
                if ok_choice_c:
                    player.socket.send('true'.encode())
                else:
                    player.socket.send('false'.encode())
            chosen_cards.append(choice)
            possible_choices.remove(choice)
            player.socket.send('false'.encode())
        ok_choice_cards = True
        player.socket.send('true'.encode())
        player.hand_str = possible_choices
        player.socket.send(show_line(possible_choices, 'Vous avez choisi : ').encode())
    return chosen_cards


def trade_2(nb_cards):
    possible_choices = []
    for b in board:
        possible_choices.append(b)
    remove_el(possible_choices, "chameau")
    chosen_cards = []
    for i in range(0, nb_cards):
        ok_choice = False
        while not ok_choice:
            show_line(possible_choices, 'Choix possibles : ')
            show_line(chosen_cards, 'Cartes choisies : ')
            choice = input("Choisissez une carte\n")
            ok_choice = (choice in possible_choices)
        possible_choices.remove(choice)
        chosen_cards.append(choice)
    for c in chosen_cards:
        board.remove(c)
    return chosen_cards


def trade(player):
    chosen_cards_hand = trade_1(player)
    chosen_cards_board = trade_2(len(chosen_cards_hand))
    for c in chosen_cards_board:
        player.add_hand(c)
    print("échange effectué")


def take_camels(player):
    nb_camels_on_board = board.count("chameau")
    player.take_camels(nb_camels_on_board)
    remove_el(board, "chameau")
    player.socket.send(str(nb_camels_on_board).encode())
    player.oponent_socket.send(f'Votre adversaire a pris {nb_camels_on_board} chameaux'.encode())
    return board


def take_card(player):
    valid_choice = False
    choice = ""
    while not valid_choice:
        show_board()
        choice = player.socket.recv(2048).encode
        valid_choice = (choice in board)
        if valid_choice:
            player.socket.send('true'.encode())
        else:
            player.socket.send('false'.encode())
    board.remove(choice)
    player.take_card(choice)


def buy_ressource_1(player):
    ok_buy = False
    while not ok_buy:
        res = player.socket.recv(2048).decode
        c = int(player.socket.recv(2048).decode)
        ok_buy = buy_ressource_2(res, c, player)
        if ok_buy:
            player.socket.send('true'.encode())
        else:
            player.socket.send('false'.encode())
    player.socket.send(f'votre score est maintenant {player.score}'.encode())


def buy_ressource_2(ressource, nb, player):
    ok_buy = False
    if player.buy(ressource, nb):
        count = min(nb, len(ressources[ressource]))
        for i in range(count):
            s = ressources[ressource].pop()
            player.add_score(s)
        if len(bonus[count]) >= 1:
            player.add_score(bonus[count].pop())
        print("Vente effectuée")
        ok_buy = True
    else:
        print("Vente impossible")
    return ok_buy


def end_turn():
    if len(board) < 5:
        for i in range(0, 5-len(board)):
            card = deck.pop()
            board.append(card)


def show_board():
    strn = ''
    for b in board:
        strn += b + ', '
    return f'Marché : {strn}'


def show_ressources():
    sf = "Ressources"
    for key, value in ressources.items():
        strn = ""
        for v in value:
            strn += str(v) + ', '
        sf += f'{key}: {strn}\n'
    return sf


def turn(player):
    print(f'Tour de {player.name}')
    player.socket.send(player.show_hand().encode())

    print(f'Vous avez {player.nb_camel} chameaux')
    print(f'Votre score est {player.score}')
    show_board()
    show_ressources()
    possible_input = ('prendre', 'échanger', 'vendre', 'chameaux')
    success_choice = False
    while not success_choice:
        print('Choix possibles : prendre, échannger, vendre ou chameaux')
        choice = player.socket.recv(2048).decode()
        if choice == "prendre":
            success_choice = player.ok_choice_take_card()
        elif choice == 'échanger':
            success_choice = player.ok_choice_trade()
        elif choice == 'vendre':
            success_choice = player.ok_choice_sell()
        elif choice == 'chameaux':
            success_choice = board.count('chameau') > 0
        if success_choice:
            player.socket.send(('true').encode())
        else:
            player.socket.send(('false').encode())

    if choice == "prendre":
        take_card(player)
    elif choice == "échanger":
        trade(player)
    elif choice == 'vendre':
        buy_ressource_1(player)
    elif choice == 'chameaux':
        take_camels(player)


def end_game():
    c = 0
    for key, value in ressources.items():
        if len(value) == 0:
            c += 1
    return c >= 3 or len(deck) == 0


def fill_board():
    if len(board) <5:
        for i in range(5 - len(board)):
            board.append(deck.pop())


def deal_hand(player):
    for i in range(5):
        player.take_card(deck.pop())

    for c in player.hand_str:
        if c == 'chameau':
            player.hand_str.remove('chameau')
            player.nb_camel += 1


def setup_game():
    shuffle_deck()
    fill_board()


def new_game():
    name1 = client1.recv(2048).decode()
    print(f'Premier joueur : {name1} \n')
    name2 = client2.recv(2048).decode()
    print(f'Second joueur : {name2} \n')
    joueur1 = Player(name1, client1, client2)
    joueur2 = Player(name2, client2, client1)
    setup_game()
    deal_hand(joueur1)
    deal_hand(joueur2)
    b = show_board()
    h1 = joueur1.show_hand()
    h2 = joueur2.show_hand()
    joueur1.socket.send(b.encode())
    joueur1.socket.recv(2048)
    joueur2.socket.send(b.encode())
    joueur2.socket.recv(2048)
    print('On a envoyé le board aux deux joueurs \n')
    joueur1.socket.send(h1.encode())
    joueur1.socket.recv(2048)
    print('main j1 envoyée')
    joueur2.socket.send(h2.encode())
    joueur2.socket.recv(2048)
    print('main j2 envoyée')
    print('On a envoyé leurs mains aux deux joueurs \n')
    while not end_game():
        b = show_board()
        r = show_ressources()
        s = 'votre'
        d = 'nv'
        client1.send(s.encode())
        client1.recv(2048)
        client2.send(d.encode())
        client1.send(b.encode())
        print('On a tout envoyé 1')
        client1.send(r.encode())
        client2.send(b.encode())
        client2.send(r.encode())
        print('On a tout envoyé 2')
        print("Début tour j1")
        turn(joueur1)
        f = 'fin'
        client2.send(f.encode())
        print('Envoyé signal de fin de tour à J2')
        fill_board()

        client1.send(d.encode())
        client2.send(s.encode())
        client1.send(b.encode())
        client1.send(r.encode())
        client2.send(b.encode())
        client2.send(r.encode())
        print('Données toutes envoyées')
        print('Début tour j2')
        turn(joueur2)
        client1.send(f.encode())
        print('Signal de fin envoyé à j1')
        fill_board()

new_game()
