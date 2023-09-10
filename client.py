# -*- coding: utf8 -*-

import socket

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8000

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_client.connect((SERVER_ADDRESS, SERVER_PORT))

#enviar ping para o servidor
socket_client.sendall(b'ping!')

dado = socket_client.recv(1024)
dado = dado.decode()

print(f'recebido do servidor {dado}')

print('conexão estbelecida com sucesso.')

socket_client.close()