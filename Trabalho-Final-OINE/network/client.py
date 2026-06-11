# network/client.py
import socket
import json
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from network_settings import PORT, SERVER_IP, FORMAT, BUFFER_SIZE

class GameClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.latest_messages = [] # Fila de mensagens para o Pygame processar

    def connect(self, ip=SERVER_IP):
        try:
            self.client.connect((ip, PORT))
            self.connected = True
            
            # Inicia a thread que fica escutando o servidor
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True # Garante que a thread feche se o jogo fechar
            receive_thread.start()
            
            return True
        except Exception as e:
            print(f"[ERRO CLIENTE] Falha ao conectar: {e}")
            return False

    def receive_messages(self):
        """Roda em background escutando o servidor."""
        while self.connected:
            try:
                msg_raw = self.client.recv(BUFFER_SIZE).decode(FORMAT)
                if msg_raw:
                    data = json.loads(msg_raw)
                    self.latest_messages.append(data)
            except Exception as e:
                print(f"[ERRO CLIENTE] Conexão com servidor perdida.")
                self.connected = False
                break

    def get_messages(self):
        """Retorna as mensagens recebidas e limpa a fila."""
        msgs = self.latest_messages.copy()
        self.latest_messages.clear()
        return msgs

    def send_data(self, data: dict):
        if self.connected:
            try:
                msg_json = json.dumps(data)
                self.client.send(msg_json.encode(FORMAT))
            except Exception as e:
                print(f"[ERRO CLIENTE] Falha ao enviar: {e}")

    def disconnect(self):
        if self.connected:
            self.send_data({"type": "disconnect"})
            self.connected = False
            self.client.close()