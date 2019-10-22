import socket
hote = 'localhost'
port = 8001
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("connecté")


def new_recv():
    msg = connexion_avec_serveur.recv(2048).decode()
    print(f'message reçu {msg}')
    dd = 'ok'
    connexion_avec_serveur.send(dd.encode())
    print('confirmation envoyée')
    return msg


def new_send(msg):
    connexion_avec_serveur.send(msg.encode())
    print('message envoyée')
    ro = connexion_avec_serveur.recv(2048).decode()
    print('confirmation reçue')


end = False
name = input("Quel est votre nom ?:\n")
new_send(name)
print('Nom envoyé, on attend le board')
board = new_recv()
print(board)
print('board reçu, on attend la main')
hand = new_recv()
print(hand)
while not end:
    tour = new_recv()
    print(f'\n tour recu : {tour}')
    board = new_recv()
    ressources = new_recv()
    print(board, '\n')
    print(ressources, '\n')
    print(tour, '\n')
    if tour == 'votre':
        print("C'EST TON TOUR WESH")
        hand = new_recv()
        print(hand, '\n')
        possible_choice = ''
        choice = ''
        while possible_choice != "true":
            choice = input('Choisissez parmi vendre, échanger, chameaux ou prendre\n')
            new_send(choice)
            possible_choice = new_recv()
            print(possible_choice)

        if choice == 'vendre':
            ok_sell = False
            while not ok_sell:
                choice = input("Quelle matière vendre ?\n")
                new_send(choice)
                quantity = input('Quelle quantité ?\n')
                new_send(quantity)
                ok_sell = (new_recv() == 'true')
            print(new_recv())
        elif choice == 'chameaux':
            nb = new_recv()
            nb = int(nb)
            print(f'Vous avez récupéré {nb} chameaux')
        elif choice == 'échanger':
            ok_pre_trade = False
            while not ok_pre_trade:
                ok_chameaux = False
                while not ok_chameaux:
                    nb_cham = input("Combien de chameaux voulez-vous échanger ?\n")
                    ok_chameaux = (new_recv() == 'true')
                ok_cards = False
                while not ok_cards:
                    nb_cards = input("Combien de cartes voulez-vous échanger ?\n")
                    ok_cards = (new_recv() == 'true')
                ok_pre_trade = (new_recv() == 'true')
            ok_trade = False
            while not ok_trade:
                possible_choice = new_recv()
                chosen_cards = new_recv()
                print(possible_choice)
                print(chosen_cards)
                ok_choice_c = False
                while not ok_choice_c:
                    print(new_recv())
                    choice = input('Quelle carte donner ?\n')
                    new_send(choice)
                    if new_recv() == 'true':
                        ok_choice_c = True
                    else:
                        ok_choice_c = False
                ok_trade = (new_recv() == 'true')
                print(new_recv())
        elif choice == 'prendre':
            ok_take = ""
            while ok_take != 'true':
                    choice = input("Quelle carte prendre ?\n")
                    new_send(choice)
                    ok_take = new_recv()



    else:
        print("C'est pas ton tour wesh")
        end_turn = False
        while not end_turn:
            strn = new_recv()
            if strn == 'fin':
                end_turn = True
            else:
                print(strn)
