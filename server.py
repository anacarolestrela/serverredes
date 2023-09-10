# Referência: https://www.youtube.com/watch?v=UpKim6rFFQE&t=176s

import socket
import sys

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8000

def handle_request(socket_cliente):
    # Recebendo dados do cliente
    dado_recebido = socket_cliente.recv(1024)  # Até 1024 bytes
    dado_recebido = dado_recebido.decode()

    # Parsing do cabeçalho
    headers = dado_recebido.split('\r\n')
    header_get = headers[0]  # Pega a primeira linha do cabeçalho

    # Capturar o arquivo que foi solicitado
    arquivo_solicitado = header_get.split(' ')[1][1:]  # Pega a segunda palavra da linha a partir do segundo caractere
    print(f'Arquivo solicitado: {arquivo_solicitado}')
    if arquivo_solicitado == '':
        arquivo_solicitado = 'index.html'

    # Abrir arquivo
    try:
        file = open(arquivo_solicitado, 'r', encoding='utf-8')
        conteudo_arquivo = file.read()
    except FileNotFoundError:
        print(f'Arquivo não existe: {arquivo_solicitado}')
        # Retorna erro 404
        socket_cliente.sendall(b'HTTP/1.1 404 File not found\r\n\r\nFile not found')
        socket_cliente.close()
        return

    # Enviar conteúdo do arquivo para o navegador
    cabecalho_resposta = f'HTTP/1.1 200 OK\r\n\r\n'
    corpo_resposta = conteudo_arquivo

    resposta_final = cabecalho_resposta + corpo_resposta

    # Responde ao cliente
    socket_cliente.sendall(resposta_final.encode('utf-8'))  # sendall faz o destino não esperar por mais dados 

    # Encerrando conexão
    socket_cliente.close()

# Criando objeto socket
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Argumentos: 1- TCP, 2- IP

# Solicitar ao Windows para ouvir a porta 8000
socket_server.bind((SERVER_ADDRESS, SERVER_PORT))  # 0.0.0.0 vai ouvir em todas as placas de redes disponíveis, 8000 é a porta
socket_server.listen()

# Aguardar conexão com cliente
# Debug
print(f'Servidor ouvindo em {SERVER_ADDRESS}:{SERVER_PORT} pronto para receber conexões...')

while True:
    socket_cliente, cliente_addr = socket_server.accept()

    # Debug
    print(f'Cliente conectado com sucesso. {cliente_addr[0]}:{cliente_addr[1]}')

    # Lidar com cada solicitação em uma função separada
    handle_request(socket_cliente)
