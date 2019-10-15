from player import *
from card import *

ressources = {"rubis": [], "or": [], "argent": [], "épices": [], "cuir": []}
board = []

def buy_ressource(dict_ressources, ressource, nb, player):
    if player.buy(ressource, nb):
        count = min(nb, dict_ressources[ressource].len())
        for i in range(0, count):
            s = dict_ressources[ressource].pop()
            player.add_score(s)
        print("Achat effectué")
    else:
        print("Achat impossible")
    return dict_ressources

def turn(player):
    possible_input = ('prendre', 'échanger', 'acheter', 'chameaux')
    choice = input('faites votre choix parmi les options autorisées')
name1 = input("Nom du joueur 1")
name2 = input("Nom du joueur 2")
joueur1 = Player(name1)
joueur2 = Player(name2)