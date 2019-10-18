from player import *
from card import *
import random

from data import *


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
    print(mess, str)


def trade_1(player):
    ok_pre_trade = False
    nb_camels_trade = 0
    nb_cards_trade = 0
    while not ok_pre_trade:
        ok_camels = False
        while not ok_camels:
            nb_camels_trade = int(input("Combien de chameaux voulez-vous échanger ?\n"))
            if 0 <= nb_camels_trade <= player.nb_camel:
                ok_camels = True
            else:
                print("Nombre de chameaux non valide")
        ok_cards = False
        while not ok_cards:
            nb_cards_trade = int(input("Combien de cartes voulez-vous échanger ?\n"))
            if 0<= nb_cards_trade <= len(player.hand_str):
                ok_cards = True
            else:
                print("Nombre de cartes non valide")
        total_trade = nb_camels_trade + nb_cards_trade
        if 2 <= total_trade <= (5 - board.count("chameau")):
            ok_pre_trade = True
        else:
            print("Les données de l'échange ne sont pas valides")
    ok_choice_cards = False
    chosen_cards = []
    while not ok_choice_cards:
        chosen_cards = []
        possible_choices = player.hand_str
        for i in range(0, nb_cards_trade):
            show_line(possible_choices, 'Choix possibles : ')
            show_line(chosen_cards, 'Cartes choisies : ')
            ok_choice_c = False
            choice = ''
            while not ok_choice_c:
                choice = input("Choisissez une carte\n")
                ok_choice_c = (choice in possible_choices)
            chosen_cards.append(choice)
            possible_choices.remove(choice)
        ok_choice_cards = True
        player.hand_str = possible_choices
        show_line(possible_choices, 'Vous avez choisi : ')
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
    return board


def take_card(player):
    valid_choice = False
    choice = ""
    while not valid_choice:
        show_board()
        choice = input("Quelle carte prendre ?")
        valid_choice = (choice in board)
    board.remove(choice)
    player.take_card(choice)


def buy_ressource_1(player):
    ok_buy=False
    while not ok_buy:
        res = input("Quelle ressource vendre ?")
        c = int(input("Quelle quantité ?"))
        ok_buy = buy_ressource_2(res, c, player)


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
    print(f'Marché : {strn}')

def show_ressources():
    print('Ressources')
    for key, value in ressources.items():
        strn = ""
        for v in value:
            strn += str(v) + ', '
        print(f'{key}: {strn}')


def turn(player):
    print(f'Tour de {player.name}')
    player.show_hand()
    print(f'Vous avez {player.nb_camel} chameaux')
    print(f'Votre score est {player.score}')
    show_board()
    show_ressources()
    possible_input = ('prendre', 'échanger', 'vendre', 'chameaux')
    success_choice = False
    while not success_choice:
        print('Choix possibles : prendre, échannger, vendre ou chameaux')
        choice = input('faites votre choix parmi les options autorisées\n')
        if choice == "prendre":
            success_choice = player.ok_choice_take_card()
        elif choice == 'échanger':
            success_choice = player.ok_choice_trade()
        elif choice == 'vendre':
            success_choice = player.ok_choice_sell()
        elif choice == 'chameaux':
            success_choice = board.count('chameau') > 0

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
    name1 = input("Nom du joueur 1\n")
    name2 = input("Nom du joueur 2\n")
    joueur1 = Player(name1)
    joueur2 = Player(name2)
    setup_game()
    deal_hand(joueur1)
    deal_hand(joueur2)
    while not end_game():
        turn(joueur1)
        fill_board()
        turn(joueur2)
        fill_board()

new_game()