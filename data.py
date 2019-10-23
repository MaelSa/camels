ressources = {"diamants": [5, 5, 5, 7, 7], "or": [5, 5, 5, 6, 6], "argent": [5, 5, 5, 5, 5],
              "tissus": [1, 1, 2, 2, 3, 3, 5],
              "épices": [1, 1, 2, 2, 3, 3, 5], "cuir": [1, 1, 1, 1, 1, 1, 2, 3, 4]}
bonus = {1: [], 2: [], 3: [1, 1, 2, 2, 2, 3, 3], 4: [4, 4, 5, 5, 6, 6], 5: [8, 8, 9, 10, 10]}
diamonds = ["diamants" for i in range(6)]
gold = ["or" for i in range(6)]
silver = ["argent" for i in range(6)]
tissus = ["tissus" for i in range(8)]
epices = ["épices" for i in range(8)]
cuir = ['cuir' for i in range(10)]
camels = ['chameau' for i in range(11)]
board = []
deck = diamonds + gold + silver + tissus + epices + cuir + camels