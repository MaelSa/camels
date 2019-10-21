import socket
hote = 'localhost'
port = 8000
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("connecté")


end = False
name = input("Quel est votre nom ?:\n")
connexion_avec_serveur.send(name.encode())
print('Nom envoyé, on attend le board')
board = connexion_avec_serveur.recv(2048).decode()
connexion_avec_serveur.send(board.encode())
print(board)
print('board reçu, on attend la main')
hand = connexion_avec_serveur.recv(2048).decode()
connexion_avec_serveur.send(hand.encode())
print(f'Votre main est : {hand} \n')
while not end:
    tour = connexion_avec_serveur.recv(2048).decode()
    print(f'\n tour recu : {tour}')
    board = connexion_avec_serveur.recv(2048).decode()
    ressources = connexion_avec_serveur.recv(2048).decode()
    print(board, '\n')
    print(ressources, '\n')
    print(tour, '\n')
    if tour == 'votre':
        hand = connexion_avec_serveur.recv(2048).decode()
        print(hand, '\n')
        possible_choice = ''
        choice = ''
        while possible_choice != "true":
            choice = input('Choisissez parmi vendre, échanger, chameaux ou prendre\n')
            connexion_avec_serveur.send(choice.encode())
            possible_choice = connexion_avec_serveur.recv(2048).decode()
            print(possible_choice)

        if choice == 'vendre':
            ok_sell = False
            while not ok_sell:
                choice = input("Quelle matière vendre ?\n")
                connexion_avec_serveur.send(choice.encode())
                quantity = input('Quelle quantité ?\n')
                connexion_avec_serveur.send(quantity.encode())
                ok_sell = (connexion_avec_serveur.recv(2048).decode() == 'true')
            print(connexion_avec_serveur.recv(2048).decode())
        elif choice == 'chameaux':
            nb = connexion_avec_serveur.recv(2048).decode()
            nb = int(nb)
            print(f'Vous avez récupéré {nb} chameaux')
        elif choice == 'échanger':
            ok_pre_trade = False
            while not ok_pre_trade:
                ok_chameaux = False
                while not ok_chameaux:
                    nb_cham = input("Combien de chameaux voulez-vous échanger ?\n")
                    ok_chameaux = (connexion_avec_serveur.recv(2048).decode() == 'true')
                ok_cards = False
                while not ok_cards:
                    nb_cards = input("Combien de cartes voulez-vous échanger ?\n")
                    ok_cards = (connexion_avec_serveur.recv(2048).decode() == 'true')
                ok_pre_trade = (connexion_avec_serveur.recv(2048).decode() == 'true')
            ok_trade = False
            while not ok_trade:
                possible_choice = connexion_avec_serveur.recv(2048).decode()
                chosen_cards = connexion_avec_serveur.recv(2048).decode()
                print(possible_choice)
                print(chosen_cards)
                ok_choice_c = False
                while not ok_choice_c:
                    print(connexion_avec_serveur.recv(2048).decode())
                    choice = input('Quelle carte donner ?\n')
                    connexion_avec_serveur.send(choice.encode())
                    if connexion_avec_serveur.recv(2048).decode() == 'true':
                        ok_choice_c = True
                    else:
                        ok_choice_c = False
                ok_trade = (connexion_avec_serveur.recv(2048).decode() == 'true')
                print(connexion_avec_serveur.recv(2048).decode())
        elif choice == 'prendre':
            ok_take = ""
            while ok_take != 'true':
                    choice = input("Quelle carte prendre ?\n")
                    connexion_avec_serveur.send(choice.encode())
                    ok_take = connexion_avec_serveur.recv(2048).decode()



    else:
        end_turn = False
        while not end_turn:
            strn = connexion_avec_serveur.recv(2048).decode()
            if strn == 'fin':
                end_turn = True
            else:
                print(strn)
