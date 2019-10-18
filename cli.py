import socket
hote = 'localhost'
port = 5000
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("connecté")
ts = input("dd")
connexion_avec_serveur.send(ts.encode())