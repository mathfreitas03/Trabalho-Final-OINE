# network/server.py
import socket
import threading
import json
import sys
import os

# Adiciona a raiz do projeto ao path para importar as configurações corretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from network_settings import PORT, SERVER_IP, ADDR, FORMAT, BUFFER_SIZE

class GameServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Garante a liberação rápida da porta
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Diz ao Windows para aceitar conexões vindas de QUALQUER IP local nesta porta
        self.socket.bind(("", PORT)) 
        # Listas de controle de conexões
        self.clients = []
        self.players_info = [] # Guarda os dados de quem está na sala

    def broadcast(self, data: dict):
        """Envia uma mensagem JSON para TODOS os clientes conectados."""
        msg_json = json.dumps(data)
        for client in self.clients:
            try:
                client.send(msg_json.encode(FORMAT))
            except Exception as e:
                print(f"[ERRO BROADCAST] Falha ao enviar para um cliente: {e}")

    def handle_client(self, conn, addr):
        print(f"[NOVA CONEXÃO] {addr} entrou no servidor.")
        connected = True
        
        while connected:
            try:
                msg_raw = conn.recv(BUFFER_SIZE).decode(FORMAT)
                if not msg_raw:
                    break
                
                data = json.loads(msg_raw)
                msg_type = data.get("type")
                
                if msg_type == "join":
                    # Um novo jogador mandou seus dados do Lobby
                    player_data = {
                        "id": str(addr), # Usamos o endereço como ID único temporário
                        "name": data.get("name"),
                        "class": data.get("class")
                    }
                    self.players_info.append(player_data)
                    print(f"[SALA] {player_data['name']} ({player_data['class']}) entrou na sala.")
                    
                    # Avisa todo mundo que a lista de jogadores atualizou
                    self.broadcast({
                        "type": "lobby_update",
                        "players": self.players_info
                    })
                    
                elif msg_type == "start_game":
                    print("[SALA] O Host iniciou a partida!")
                    self.broadcast({"type": "game_start"})
                    
                elif msg_type == "disconnect":
                    connected = False
                    
            except json.JSONDecodeError:
                pass
            except Exception as e:
                print(f"[ERRO] Conexão perdida com {addr}: {e}")
                break

        # Limpeza quando o cliente desconecta
        if conn in self.clients:
            self.clients.remove(conn)
        
        # Remove o jogador da lista e avisa os outros
        self.players_info = [p for p in self.players_info if p["id"] != str(addr)]
        self.broadcast({
            "type": "lobby_update",
            "players": self.players_info
        })
        
        conn.close()
        print(f"[DESCONEXÃO] {addr} saiu.")

    def start(self):
        self.socket.listen()
        print(f"[INICIADO] Servidor CodeQuest rodando em {SERVER_IP}:{PORT}")
        
        while True:
            # Alterado de self.server.accept() para self.socket.accept()
            conn, addr = self.socket.accept()
            self.clients.append(conn)
            
            # Cria uma thread para cuidar desse jogador específico
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = GameServer()
    server.start()