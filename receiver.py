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

# As linhas abaixo executam o parseamento dos argumentos de entrada
parser = argparse.ArgumentParser()
parser.add_argument("-porta", required=True, help="Porta do servidor. Valores válidos entre 10001 e 11000", type=int)
args = vars(parser.parse_args())
receiver_port = args['porta']

# Verificação dos argumentos de entrada
if receiver_port < 10001 or receiver_port > 11000:
    print("A porta %d é inválida. Insira um valor inteiro entre 10001 - 11000" % receiver_port)
    exit(-1)

# Criação do socket UDP
try:
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind(('', receiver_port))
    print("Receiver inicializado...")
except socket.error:
    print("Erro inicializando o receiver...")
    exit(-1)

# Inicialização de variáveis globais
sequence = 0
recv_nmsgs = 0

# Inicio do loop onde as mensagens serão recebidas e tratadas
while True:
    # Recebendo uma mensagem
    message, sender_address = receiver_socket.recvfrom(2048)
    # Parser da mensagem recebida
    recv_sequence = int(message[0:1])
    recv_data = int(message[1:2])
    recv_nmsgs = int(message[2:])

    if recv_sequence == sequence:
        # Se o valor de sequência recebido for igual ao esperado,
        # a resposta é montada com o ACK verdadeiro e o bit de sequência
        # é invertido para que a aplicação espere uma nova mensagem
        response = getResponse(True, recv_sequence)
        sequence = int(not sequence)
    else:
        # Se o valor de sequência recebido não for igual ao esperado,
        # a resposta é montada com o ACK falso, e a sequência é mantida
        # para que se aguarde uma mensagem com a sequência correta.
        response = getResponse(False, recv_sequence)
        print("Número de sequência recebido não equivale ao esperado.\
             Esperado %d, recebido %d" % (sequence, int(recv_sequence)))

    # Respondendo para o sender sobre o reconhecimento da mensagem.
    receiver_socket.sendto(response.encode(), sender_address)
    print("RECV: " + message.decode())
    print("SENT: " + response)
    print("")

    if recv_nmsgs == recv_data:
        # O campo data indica o indíce da mensagem enviada. Caso ele seja
        # igual ao número de mensagens que devem ser enviadas, isso indica
        # que é a última mensagem, e o programa deve finalizar a execução 
        exit(0)
