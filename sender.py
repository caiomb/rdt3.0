import platform
import subprocess
import argparse
from socket import *

# https://stackoverflow.com/questions/2953462/pinging-servers-in-python
def ping(host):
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

parser = argparse.ArgumentParser()
parser.add_argument("-ip", required=True, help="IP do receiver.")
parser.add_argument("-porta", required=True, help="Porta do servidor. Valores válidos entre 10001 e 11000", type=int)
parser.add_argument("-nmsg", required=True, help="Numero de mensagens a serem enviadas", type=int)
args = vars(parser.parse_args())

receiver_name = args['ip']
receiver_port = args['porta']
n_msgs = args['nmsg']

if receiver_port < 10001 or receiver_port > 11000:
    print("A porta %d é inválida. Insira um valor inteiro entre 10001 - 11000" % receiver_port)
    exit(-1)

if n_msgs <= 0:
    print("O valor de %s não é válido para número de mensagens. Insira um número inteiro maior que zero" % n_msgs)
    exit(-1)

if not ping(receiver_name):
    print("Receiver inácessível.")
    exit(-1)

#Criação do socket UDP
try:
    sender_socket = socket(AF_INET, SOCK_DGRAM)
    sender_socket.settimeout(1)
except socket.error:
    print("Falha na criação do socket...")
    exit(-1)

sent_messages = 0
sequence = 0

while sent_messages <= n_msgs:
    message = str(sequence) + str(sent_messages) + str(n_msgs)
    is_to_send = True
    while True:
        try:
            if is_to_send:
                sender_socket.sendto(message.encode(), (receiver_name, receiver_port))
                is_to_send = False
            response, server_address = sender_socket.recvfrom(2048)
        except timeout:
            print("Timeout. A mensagem será reenviada...")
            print("")
            is_to_send = True
            continue
        ACK = response[0:1]
        ACKno = response[1:2]
        if int(ACK) and (int(ACKno) == sequence):
            print("SENT: " + message)
            print("RECV: " + response.decode())
            print("")
            sequence = int(not sequence)
            break
        else:
            is_to_send = True
            print("ACK não ok para o número de sequência. Reenviando mensagem...")
            print("")
    sent_messages+=1

sender_socket.close()
exit(0)