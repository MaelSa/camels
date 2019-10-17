from player import *
from card import *
import random

from data import *


def shuffle_deck():
    random.shuffle(deck)


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def remove_el(list, el):
    for i in range(0, len(list)):
        list.remove(el)


def trade_1(player):
    ok_pre_trade = False
    nb_camels_trade = 0
    nb_cards_trade = 0
    while not ok_pre_trade:
        ok_camels = False
        while not ok_camels:
            nb_camels_trade = int(input("Combien de chameaux voulez-vous échanger ?"))
            if 0 <= nb_camels_trade <= player.nb_camel:
                ok_camels = True
            else:
                print("Nombre de chameaux non valide")
        ok_cards = False
        while not ok_cards:
            nb_cards_trade = int(input("Combien de cartes voulez-vous échanger ?"))
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
            print(f'Choix possibles : {possible_choices}')
            print(f'Cartes déjà choisies : {chosen_cards}')
            ok_choice_c = False
            choice = ''
            while not ok_choice_c:
                choice = input("Choisissez une carte")
                ok_choice_c = (choice in possible_choices)
            chosen_cards.append(choice)
            possible_choices.remove(choice)
        ok_choice_cards = True
        player.hand_str = possible_choices
    return chosen_cards


def trade_2(nb_cards):
    possible_choices = board
    remove_values_from_list(possible_choices, "chameau")
    chosen_cards = []
    for i in range(0, nb_cards):
        ok_choice = False
        while not ok_choice:
            print(f'Choix possibles {possible_choices}')
            print(f'Cartes choisies {chosen_cards}')
            choice = input("Choisissez une carte")
            ok_choice = (choice in possible_choices)
        possible_choices.remove(choice)
        chosen_cards.append(choice)
    for c in chosen_cards:
        board.remove(c)
    return chosen_cards


def take_camels(player):
    nb_camels_on_board = board.count("chameau")
    player.take_camels(nb_camels_on_board)
    remove_values_from_list(board, "chameau")
    return board


def take_card(player):
    valid_choice = False
    choice = ""
    while not valid_choice:
        print(board)
        choice = input("Quelle carte prendre ?")
        valid_choice = (choice in board)
    board.remove(choice)
    player.take_card(choice)


def buy_ressource(ressource, nb, player):
    if player.buy(ressource, nb):
        count = min(nb, len(ressources[ressource]))
        for i in range(0, count):
            s = ressources[ressource].pop()
            player.add_score(s)
        if len(bonus[count]) >= 1:
            player.add_score(bonus[count].pop())
        print("Achat effectué")
    else:
        print("Achat impossible")


def end_turn():
    if len(board) < 5:
        for i in range(0, 5-len(board)):
            card = deck.pop()
            board.append(card)


def turn(player):
    possible_input = ('prendre', 'échanger', 'vendre', 'chameaux')
    success_turn = False
    success_choice = False
    while not success_turn:
        while not success_choice:
            choice = input('faites votre choix parmi les options autorisées')
            if choice == "prendre":
                success_choice = player.ok_choice_take_card()
            elif choice == 'échanger':
                success_choice = player.ok_choice_trade()
            elif choice == 'vendre':
                success_choice = player.ok_choice_sell()
            elif choice == 'chameaux':
                success_choice = board.count('chameau') > 0


def end_game():
    c = 0
    for key, value in ressources.items():
        if len(value) == 0:
            c += 1
    return c >= 3 or len(deck) == 0


def new_game():
    name1 = input("Nom du joueur 1")
    name2 = input("Nom du joueur 2")
    joueur1 = Player(name1)
    joueur2 = Player(name2)
