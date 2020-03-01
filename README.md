## Protocolo rdt3.0 sobre sockets UDP
O projeto consiste na implementação do protocolo rdt (entrega confiável de dados)
a nível de aplicação sobre sockets UDP. Nesta versão não há checagem de checksum
das mensagens, pois isso já é feito pelo UDP, desta forma há uma simplificação
e as aplicações só fazem a checagem de mensagens duplicadas. Em resumo, o projeto
consiste em um sender que envia mensagens para um receiver, que por sua vez as
processa e as trata respondendo ACKs para o sender.

## Execução do receiver:
Para executar o receiver digite no terminal: python3 receiver.py -porta PORTA
Os argumentos válidos são:
	-porta:  Porta do receiver com valores válidos entre 10001 e 11000.

## Execução do sender:
Para executar o sender digite no terminal:
	python3 sender.py -ip IP -porta PORTA -nmsg NMSG
Os argumentos válidos são:
 	-ip:	IP do receiver.
 	-porta:	Porta do receiver. Valores válidos entre 10001 e 11000.
 	-nmsg:	Número de mensagens a serem enviadas.

## Help:
Para acessar uma explicação básica de como executar os arquivos, digite no terminal:
	python3 sender.py -h
	python3 receiver.py -h
