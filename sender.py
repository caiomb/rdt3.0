import platform
import subprocess
import argparse
from socket import *

# A função ping foi extraída do seguinte link:
# https://stackoverflow.com/questions/2953462/pinging-servers-in-python
def ping(host):
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

# As linhas abaixo executam o parseamento dos argumentos de entrada
parser = argparse.ArgumentParser()
parser.add_argument("-ip", required=True, help="IP do receiver.")
parser.add_argument("-porta", required=True, help="Porta do servidor. Valores válidos entre 10001 e 11000", type=int)
parser.add_argument("-nmsg", required=True, help="Numero de mensagens a serem enviadas", type=int)
args = vars(parser.parse_args())
receiver_name = args['ip']
receiver_port = args['porta']
n_msgs = args['nmsg']

# Verificação dos argumentos de entrada
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

# Inicialização de variáveis globais
sent_messages = 0
sequence = 0

# Inicio do loop inicial onde as mensagens serão enviadas
# O número de mensagens que devem ser enviados vai de 0 até o
# valor recebido por parâmetro
while sent_messages <= n_msgs:
    # Monta uma mensagem com a seguinte formatação SEQNO+DATA+MSGS
    message = str(sequence) + str(sent_messages) + str(n_msgs)

    # Configura a flag de envio para verdadeiro. Isso indica que a mensagem ainda não
    # foi enviada, e por isso deverá ser. 
    is_to_send = True

    # Loop infinito para enviar uma mensagem e receber a resposta do sender.
    while True:
        try:
            if is_to_send:
                # Envia a mensagem para o receiver
                sender_socket.sendto(message.encode(), (receiver_name, receiver_port))
                # Indica que a mensagem já foi enviada
                is_to_send = False
            response, server_address = sender_socket.recvfrom(2048)
        except timeout:
            # Em caso de timeout, uma mensagem é mostrada para indicar isso
            # e a flag de envio é setada para true para que a mensagem seja
            # reenviada.
            print("Timeout. A mensagem será reenviada...")
            print("")
            is_to_send = True
            continue # Força a volta ao início desse loop para que a mensagem seja reenviada

        # Neste ponto a mensagem foi enviada e uma resposta foi recebida, então deve-se fazer
        # o parser da mensagem recebida
        ACK = response[0:1]
        ACKno = response[1:2]

        if int(ACK) and (int(ACKno) == sequence):
            # Se o ACK recebido for verdadeiro e o valor da sequência recebido
            # for igual ao enviado, então o envio de dados ocorreu com sucesso.
            # Neste caso deve-se printar a mensagem e inverter o bit de sequência
            # para que uma nova mensagem seja enviada com o próximo número de sequência
            print("SENT: " + message)
            print("RECV: " + response.decode())
            print("")
            sequence = int(not sequence)
            break # O break abaixo encerra a execução desse loop
        else:
            # Se o ACK recebido for falso ou se o valor da sequência recebido
            # não for igual ao esperado, então o envio de dados não foi bem
            # sucedido. Neste caso a flag de envio de mensagem é configurado para verdadeiro 
            # para que a mensagem seja reenviada. O programa voltará ao inicio desse loop
            # para tentar reenviar a mesma mensagem.
            is_to_send = True
            print("ACK não ok para o número de sequência. Reenviando mensagem...")
            print("")
    # Se a aplicação chegar a este ponto, então o envio da último mensagem foi
    # bem sucedido. Deve-se então incrementar o número de mensagem enviadas, que será
    # o próximo dado, e a aplicação voltará ao início do loop inicial para montar e enviar
    # uma nova mensagem
    sent_messages+=1

# Fim do envio de todas as mensagens, o socket será fechado e a execução da aplicação finalizada.
sender_socket.close()
exit(0)