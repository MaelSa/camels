from player import *
from card import *


ressources = {"rubis": [], "or": [], "argent": [], "épices": [], "cuir": []}
board = []

def take_card(player, board):
    valid_choice = False
    while not valid_choice:
        print("Quelle carte prendre ?")
        for i in range(0, len(board)):
            print(f'{i} : {board[i]}')
        choice = int(input())
        valid_choice = (0 >= choice < len(board))


def buy_ressource(dict_ressources, ressource, nb, player):
    if player.buy(ressource, nb):
        count = min(nb, len(dict_ressources[ressource]))
        for i in range(0, count):
            s = dict_ressources[ressource].pop()
            player.add_score(s)
        print("Achat effectué")
    else:
        print("Achat impossible")
    return dict_ressources

def turn(player):
    possible_input = ('prendre', 'échanger', 'acheter', 'chameaux')
    success_turn = False
    success_choice = False
    while not success_turn:
        while not success_choice:
            choice = input('faites votre choix parmi les options autorisées')
            success_choice = (choice in possible_input)


name1 = input("Nom du joueur 1")
name2 = input("Nom du joueur 2")
joueur1 = Player(name1)
joueur2 = Player(name2)