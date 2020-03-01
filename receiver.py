import argparse
from socket import *

def getResponse(ACK, recv_sequence):
    # Prepara a resposta com o ACK para sequência e concatena
    # com o número de sequência:
    #   ACK=1 | NACK=0
    if ACK:
        response = str(1)
    else:
        response = str(0)
    return response + str(recv_sequence)

parser = argparse.ArgumentParser()
parser.add_argument("-porta", required=True, help="Porta do servidor. Valores válidos entre 10001 e 11000", type=int)
args = vars(parser.parse_args())
receiver_port = args['porta']

if receiver_port < 10001 or receiver_port > 11000:
    print("A porta %d é inválida. Insira um valor inteiro entre 10001 - 11000" % receiver_port)
    exit(-1)

try:
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind(('', receiver_port))
    print("Receiver inicializado...")
except socket.error:
    print("Erro inicializando o receiver...")
    exit(-1)

sequence = 0
recv_nmsgs = 0

while True:
    message, sender_address = receiver_socket.recvfrom(2048)
    recv_sequence = int(message[0:1])
    recv_data = int(message[1:2])
    recv_nmsgs = int(message[2:])

    if recv_sequence == sequence:
        response = getResponse(True, recv_sequence)
        sequence = int(not sequence)
    else:
        response = getResponse(False, recv_sequence)
        print("Número de sequência recebido não equivale ao esperado. \
                Esperado %d, recebido %d" % (sequence, int(recv_sequence)))

    receiver_socket.sendto(response.encode(), sender_address)
    print("RECV: " + message.decode())
    print("SENT: " + response)
    print("")

    if recv_nmsgs == recv_data:
        exit(0)
