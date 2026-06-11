import socket

PORT = 9999

# Descobre o IP local da máquina dinamicamente
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) # Conexão temporária para puxar a interface ativa
    SERVER_IP = s.getsockname()[0]
    s.close()
except Exception:
    SERVER_IP = "127.0.0.1" # Fallback caso offline

ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 2048
DISCONNECT_MESSAGE = "!DISCONNECT"