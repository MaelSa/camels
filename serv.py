import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(('', 5000))
conn.listen(5)

client, adress = conn.accept()
print("wewconnect")
received = client.recv(255).decode()
print(received)