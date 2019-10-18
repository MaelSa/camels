import socket
hote = 'localhost'
port = 5000
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("connecté")
ts = input("dd")
connexion_avec_serveur.send(ts.encode())

end = False
name = input("Quel est votre nom ?:\n")
(board, hand) = connexion_avec_serveur.recv(255).decode()
print(f'Le marché est : {board}')
print(f'Votre main est : {hand}')
while not end:
    tour = connexion_avec_serveur.recv(255).decode()
    (board, ressources) = connexion_avec_serveur.recv(255).decode()
    print(board)
    print(ressources)
    if tour:
        hand = connexion_avec_serveur.recv(255).decode()
        print(hand)
        possible_choice = False
        while not possible_choice
            choice = input('Choisissez parmi vendre, échanger, chameaux ou prendre\n')
            connexion_avec_serveur.send(choice.encode())
            possible_choice = connexion_avec_serveur.recv(255).decode()

        if choice == 'vendre':
        elif choice == 'chameaux':
            nb = connexion_avec_serveur.recv(255).decode()
            print(f'Vous avez récupéré {nb} chameaux')
        elif choice == 'échanger':
        elif choice == 'prendre':
            ok_take = False
            while not ok_take:
                    choice = input("Quelle carte prendre ?\n")
                    connexion_avec_serveur.send(choice.encode())




    else:
        end_turn = False
        while not end_turn:
            strn = connexion_avec_serveur.recv(255).decode()
            if strn == 'fin':
                end_turn = True
            else:
                print(strn)
