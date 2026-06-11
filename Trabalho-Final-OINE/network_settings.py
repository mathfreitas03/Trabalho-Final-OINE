# network_settings.py
import socket

# Configurações globais do TCP
PORT = 5050

# Pega o IP local da máquina automaticamente (Essencial para o host LAN)
SERVER_IP = "10.90.33.143"

ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 2048
DISCONNECT_MESSAGE = "!DISCONNECT"