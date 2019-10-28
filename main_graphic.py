# coding=utf-8
from player import *
from card import *
import random
import socket
from data import *


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


def trade_1(player):
    ok_pre_trade = False
    nb_camels_trade = 0
    nb_cards_trade = 0
    while not ok_pre_trade:
        ok_camels = False
        while not ok_camels:
            nb_camels_trade = int(new_recv(player.socket))
            if 0 <= nb_camels_trade <= min(player.nb_camel, 5-len(player.hand_str)):
                ok_camels = True
                new_send(player.socket, 'true')
            else:
                print("Nombre de chameaux non valide")
                new_send(player.socket, 'false')
        ok_cards = False
        while not ok_cards:
            nb_cards_trade = int(new_recv(player.socket))
            if 0 <= nb_cards_trade <= len(player.hand_str):
                ok_cards = True
                new_send(player.socket, 'true')
            else:
                print("Nombre de cartes non valide")
                new_send(player.socket, 'false')
        total_trade = nb_camels_trade + nb_cards_trade
        if 2 <= total_trade <= (5 - board.count("chameau")):
            ok_pre_trade = True
            new_send(player.socket, 'true')
        else:
            print("Les données de l'échange ne sont pas valides")
            new_send(player.socket, 'false')
    ok_choice_cards = False
    chosen_cards = []
    while not ok_choice_cards:
        chosen_cards = []
        possible_choices = player.hand_str
        for i in range(0, nb_cards_trade):
            new_send(player.socket, show_line(possible_choices, 'Choix possibles : '))
            new_send(player.socket, show_line(chosen_cards, 'Cartes choisies : '))
            ok_choice_c = False
            choice = ''
            while not ok_choice_c:
                new_send(player.socket, 'Choix ?')
                choice = new_recv(player.socket)
                ok_choice_c = (choice in possible_choices)
                if ok_choice_c:
                    new_send(player.socket, 'true')
                else:
                    new_send(player.socket, 'false')
            chosen_cards.append(choice)
            possible_choices.remove(choice)

        print('On quitte la donation')
        ok_choice_cards = True
        player.hand_str = possible_choices
        new_send(player.socket, show_line(chosen_cards, 'Vous avez choisi : '))
    return chosen_cards, total_trade


def trade_2(nb_cards, player):
    print('On commence à prendre pépouze')
    new_send(player.socket, str(nb_cards))
    possible_choices = []
    for b in board:
        possible_choices.append(b)
    remove_el(possible_choices, "chameau")
    chosen_cards = []
    for i in range(0, nb_cards):
        ok_choice = False
        while not ok_choice:
            new_send(player.socket, show_line(possible_choices, 'Choix possibles : '))
            new_send(player.socket, show_line(chosen_cards, 'Cartes choisies : '))
            print('on attend un choice')
            choice = new_recv(player.socket)
            print('On a eu le choice')
            ok_choice = (choice in possible_choices)
            if ok_choice:
                print('on a du true sur le choice')
                new_send(player.socket, 'true')
            else:
                print('On a du false sur le choice')
                new_send(player.socket, 'false')
        print('11')
        possible_choices.remove(choice)
        chosen_cards.append(choice)
    for c in chosen_cards:
        board.remove(c)
    return chosen_cards


def trade(player):
    chosen_cards_hand, total_trade = trade_1(player)
    chosen_cards_board = trade_2(total_trade, player)
    for c in chosen_cards_board:
        player.add_hand(c)
    str_chosen = show_line(chosen_cards_hand, "")
    str_chosen_board = show_line(chosen_cards_board, "")
    new_send(player.oponent_socket, f"Votre adversaire a pris {str_chosen_board} et a ajouté {str_chosen} sur le marché")
    new_send(player.socket, f"Vous avez bien échangé {str_chosen_board} contre {str_chosen}")
    print("échange effectué")


def take_camels(player):
    nb_camels_on_board = board.count("chameau")
    player.take_camels(nb_camels_on_board)
    remove_el(board, "chameau")
    new_send(player.socket, str(nb_camels_on_board))
    new_send(player.oponent_socket, f'Votre adversaire a pris {nb_camels_on_board} chameaux')
    return board


def take_card(player):
    valid_choice = False
    choice = ""
    while not valid_choice:
        show_board()
        choice = new_recv(player.socket)
        valid_choice = (choice in board)
        if valid_choice:
            new_send(player.socket, 'true')
            new_send(player.oponent_socket, f"Carte prise par l'adversaire : {choice}")
        else:
            player.socket.send('false'.encode())
            new_send(player.socket, 'false')

    board.remove(choice)
    player.take_card(choice)


def buy_ressource_1(player):
    ok_buy = False
    while not ok_buy:
        res = new_recv(player.socket)
        c = int(new_recv(player.socket))
        ok_buy = buy_ressource_2(res, c, player)
        if ok_buy:
            new_send(player.socket, 'true')
        else:
            new_send(player.socket, 'false')
    new_send(player.socket, f'votre score est maintenant {player.score}')


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
        new_send(player.oponent_socket, f"Votre adversaire a acheté {count} {ressource}")
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
    new_send(player.socket, player.show_hand())
    print(f'Vous avez {player.nb_camel} chameaux')
    new_send(player.oponent_socket, f'Adversaire a {player.nb_camel} chameaux')
    print(f'Votre score est {player.score}')
    show_board()
    show_ressources()
    possible_input = ('prendre', 'échanger', 'vendre', 'chameaux')
    success_choice = False
    while not success_choice:
        print('Choix possibles : prendre, échannger, vendre ou chameaux')
        choice = new_recv(player.socket)
        new_send(player.oponent_socket, f"Choix de l'adversaire : {choice}")
        if choice == "prendre":
            success_choice = player.ok_choice_take_card()
        elif choice == 'échanger':
            success_choice = player.ok_choice_trade()
        elif choice == 'vendre':
            success_choice = player.ok_choice_sell()
        elif choice == 'chameaux':
            success_choice = board.count('chameau') > 0
        if success_choice:
            new_send(player.socket, 'true')
        else:
            new_send(player.socket, 'false')


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
    """
    for c in player.hand_str:
        if c == 'chameau':
            player.hand_str.remove('chameau')
            player.nb_camel += 1
    """


def setup_game():
    shuffle_deck()
    shuffle_bonus()
    fill_board()


def new_game():
    name1 = new_recv(client1)
    print(f'Premier joueur : {name1}')
    name2 = new_recv(client2)
    print(f'Second joueur : {name2}')
    joueur1 = Player(name1, client1, client2)
    joueur2 = Player(name2, client2, client1)
    setup_game()
    deal_hand(joueur1)
    deal_hand(joueur2)
    b = show_board()
    h1 = joueur1.show_hand()
    h2 = joueur2.show_hand()
    print(f'Main j1 {h1}')
    print(f'Main j2 {h2}')
    new_send(joueur1.socket, b)
    new_send(joueur2.socket, b)
    new_send(joueur1.socket, h1)
    new_send(joueur2.socket, h2)
    while not end_game():
        b = show_board()
        r = show_ressources()
        s = 'votre'
        d = 'adversaire'
        new_send(client1, s)
        new_send(client2, d)
        print(f'CHam 1 : {joueur1.nb_camel}')
        print(f'CHam 2 : {joueur2.nb_camel}')
        new_send(client1, b)
        new_send(client1, r)
        new_send(client2, b)
        new_send(client2, r)
        new_send(client1, f'Vous avez {joueur1.nb_camel} chameaux')
        new_send(client2, f'Votre adversaire a {joueur1.nb_camel} chameaux')
        turn(joueur1)
        f = 'fin'
        new_send(client2, f)
        fill_board()

        new_send(client1, d)
        new_send(client2, s)
        new_send(client1, b)
        new_send(client1, r)
        new_send(client2, b)
        new_send(client2, r)
        print('Début tour j2')
        new_send(client2, f'Vous avez {joueur2.nb_camel} chameaux')
        new_send(client1, f'Votre adversaire a {joueur2.nb_camel} chameaux')
        turn(joueur2)
        new_send(client1, f)
        fill_board()
    if joueur1.score > joueur2.score:
        print("Victoire de joueur 1")
        new_send(joueur1.socket, f"Victoire, vous avez {joueur1.score} points")
        new_send(joueur2.socket, f"Défaite, vous n'avez que {joueur2.score} points")
    elif joueur2.score == joueur1.score:
        print("égalité")
    else:
        print('Victoire de joueur 2')
        new_send(joueur2.socket, f"Victoire, vous avez {joueur2.score} points")
        new_send(joueur1.socket, f"Défaite, vous n'avez que {joueur1.score} points")
new_game()
