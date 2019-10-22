import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(('', 8001))
conn.listen(5)

client, adress = conn.accept()
print("wewconnect")
received = client.recv(2048).decode()
print(received)