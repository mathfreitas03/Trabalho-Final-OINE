import socket
import threading
import json
import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Adiciona a raiz do projeto ao path para importar as configurações corretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from network_settings import PORT, SERVER_IP, ADDR, FORMAT, BUFFER_SIZE

# Configurações de SMTP 

SMTP_SERVER = "smtp.freesmtpservers.com"
SMTP_PORT = 25
SMTP_USER = "output_homework@oine.com"
SMTP_AUTH = None
EMAIL_DESTINATARIO = "professora_oine@udesc.com"

class GameServer:
    def __init__(self):
        self.classe_disponivel = {
            "knight" : True,
            "wizard" : True,
            "rogue" : True,
            "healer" : True,
            "bard" : True
        }   

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", PORT)) 
        
        self.clients = []
        self.players_info = [] 

        # Dicionário de Telemetria Pedagógica
        # Estrutura: { "id_do_jogador": { dados } }
        self.telemetry_data = {}
        self.game_start_time = None

    def broadcast(self, data: dict):
        """Envia uma mensagem JSON para TODOS os clientes conectados."""
        msg_json = json.dumps(data)
        for client in self.clients:
            try:
                client.send(msg_json.encode(FORMAT))
            except Exception as e:
                print(f"[ERRO BROADCAST] Falha ao enviar para um cliente: {e}")

    def enviar_relatorio_por_email(self):
        """Gera um relatório pedagógico em HTML com detalhes expansíveis e envia via SMTP na porta 25 (Sem TLS)."""
        print("[TELEMETRIA] Gerando relatório de desempenho da partida...")
        
        # Criação do corpo do e-mail em HTML
        html_content = """
        <html>
        <head>
            <style>
                table { font-family: Arial, sans-serif; border-collapse: collapse; width: 100%; }
                td, th { border: 1px solid #dddddd; text-align: left; padding: 10px; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                th { background-color: #4CAF50; color: white; }
                h2 { color: #333; }
                
                /* Estilização para o link expansível */
                summary { 
                    cursor: pointer; 
                    color: #1a73e8; 
                    font-weight: bold; 
                    text-decoration: underline;
                    outline: none;
                }
                summary::-webkit-details-marker { color: #1a73e8; }
                .detalhes-container { 
                    padding: 8px; 
                    background-color: #f1f3f4; 
                    margin-top: 5px; 
                    border-radius: 4px; 
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <h2>Relatório Pedagógico - Partida CodeQuest</h2>
            <p>Clique no nome do aluno para expandir e visualizar os detalhes do desempenho.</p>
            <table>
                <tr>
                    <th>Aluno (Clique para detalhes)</th>
                    <th>Classe</th>
                    <th>Perguntas Respondidas</th>
                    <th>Acertos</th>
                    <th>Erros</th>
                    <th>Taxa de Acerto</th>
                </tr>
        """

        for p_id, data in self.telemetry_data.items():
            total = data["answered"]
            acertos = data["correct"]
            erros = total - acertos
            taxa = f"{(acertos / total) * 100:.1f}%" if total > 0 else "0.0%"
            topicos_criticos = ", ".join(set(data["wrong_topics"])) if data["wrong_topics"] else "Nenhum"
            
            # Aqui assumi que você possa ter uma lista de histórico ou logs extras no seu data. 
            # Caso não tenha, usei os tópicos críticos como o detalhe oculto.
            html_content += f"""
                <tr>
                    <td>
                        <details>
                            <summary>{data['name']}</summary>
                            <div class="detalhes-container">
                                <strong>Tópicos com Dificuldade:</strong> {topicos_criticos}<br>
                                <strong>ID do Aluno:</strong> {p_id}<br>
                                <em>Dica pedagógica: Recomenda-se reforço nos tópicos listados acima.</em>
                            </div>
                        </details>
                    </td>
                    <td>{data['class']}</td>
                    <td>{total}</td>
                    <td>{acertos}</td>
                    <td>{erros}</td>
                    <td>{taxa}</td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        # Envio do e-mail preparado para servidores locais de teste (Porta 25)
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Relatório de Telemetria - CodeQuest"
            msg["From"] = SMTP_USER
            msg["To"] = EMAIL_DESTINATARIO
            
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                # Comentados para não quebrar em servidores de teste sem criptografia/senha:
                # server.starttls() 
                # server.login(SMTP_USER, SMTP_PASSWORD) 
                
                server.sendmail(SMTP_USER, EMAIL_DESTINATARIO, msg.as_string())
                
            print("[SMTP] Relatório pedagógico enviado com sucesso por e-mail para o servidor de testes!")
        except Exception as e:
            print(f"[ERRO SMTP] Falha ao enviar e-mail: {e}")

    def handle_client(self, conn, addr):
        print(f"[NOVA CONEXÃO] {addr} entrou no servidor.")
        connected = True
        p_id = str(addr)
        
        while connected:
            try:
                msg_raw = conn.recv(BUFFER_SIZE).decode(FORMAT)
                if not msg_raw:
                    break
                
                data = json.loads(msg_raw)
                msg_type = data.get("type")
                
                if msg_type == "join":
                    player_data = {
                        "id": p_id,
                        "name": data.get("name"),
                        "class" : None
                    }
                    self.players_info.append(player_data)
                    
                    # Inicializa a estrutura de telemetria para este aluno
                    self.telemetry_data[p_id] = {
                        "name": data.get("name"),
                        "class": "Não escolhida",
                        "answered": 0,
                        "correct": 0,
                        "wrong_topics": [] # Guarda os temas/conteúdos onde o aluno errou
                    }
                    
                    print(f"[SALA] {player_data['name']} entrou na sala.")
                    
                    self.broadcast({
                        "type": "lobby_update",
                        "players": self.players_info,
                        "available_classes": self.classe_disponivel
                    })
                    
                elif msg_type == "select_class":
                    classe = data["class"].lower()
                    if self.classe_disponivel[classe]:
                        for player in self.players_info:
                            if player["id"] == p_id:
                                if player["class"] is not None:
                                    self.classe_disponivel[player["class"].lower()] = True
                                player["class"] = data["class"]
                                # Atualiza a classe também na telemetria
                                if p_id in self.telemetry_data:
                                    self.telemetry_data[p_id]["class"] = data["class"]
                                break

                        self.classe_disponivel[classe] = False
                        self.broadcast({
                            "type": "lobby_update",
                            "players": self.players_info,
                            "available_classes": self.classe_disponivel
                        })
                    else:
                        conn.send(json.dumps({
                            "type": "class_denied",
                            "class": data["class"]
                        }).encode(FORMAT))
        
                elif msg_type == "start_game":
                    print("[SALA] O Host iniciou a partida!")
                    self.game_start_time = time.time()
                    self.broadcast({"type": "game_start"})
                
                # --- CAPTURA DA TELEMETRIA PEDAGÓGICA ---
                elif msg_type == "submit_answer":
                    # Espera receber: {"type": "submit_answer", "correct": True/False, "topic": "Matematica/Python"}
                    if p_id in self.telemetry_data:
                        self.telemetry_data[p_id]["answered"] += 1
                        if data.get("correct"):
                            self.telemetry_data[p_id]["correct"] += 1
                        else:
                            # Se errou, mapeia o conteúdo da questão para o professor saber onde intervir
                            topic = data.get("topic", "Geral")
                            self.telemetry_data[p_id]["wrong_topics"].append(topic)
                    
                    # Propaga o evento se o jogo precisar processar visualmente na tela de outros jogadores
                    self.broadcast(data)

                elif msg_type == "game_over":
                    # Quando o jogo terminar (ex: derrotaram o boss ou tempo acabou), dispara o e-mail
                    print("[SALA] Fim de jogo atingido.")
                    self.enviar_relatorio_por_email()
                    self.broadcast(data)
                    
                elif msg_type == "disconnect":
                    connected = False
                    
                else:
                    self.broadcast(data)
                    
            except json.JSONDecodeError:
                pass
            except Exception as e:
                print(f"[ERRO] Conexão perdida com {addr}: {e}")
                break

        # Limpeza ao desconectar
        if conn in self.clients:
            self.clients.remove(conn)
        
        self.players_info = [p for p in self.players_info if p["id"] != p_id]
        
        for p in self.players_info:
            if p["id"] == p_id and p["class"] is not None:
                self.classe_disponivel[p["class"].lower()] = True
                break
        
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
            conn, addr = self.socket.accept()
            self.clients.append(conn)
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = GameServer()
    server.start()