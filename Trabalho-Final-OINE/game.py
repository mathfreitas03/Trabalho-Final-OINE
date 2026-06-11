# game.py
import pygame
import sys
import os
import threading

# Importações separadas corretamente
from pygame_settings import WIDTH, HEIGHT, FPS, TITLE, DARK_GREY, WHITE, BLUE, HOVER_BLUE, BLACK, LIGHT_GREY
from network_settings import SERVER_IP
from network.server import GameServer
from network.client import GameClient

from ui.button import Button
from ui.textbox import TextBox
from questions import get_random_question

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init() 
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # --- ESTADOS E DADOS DO JOGADOR ---
        self.state = "MENU"
        self.player_name = ""
        self.player_class = None
        self.is_host = False
        
        # --- VARIÁVEIS DE REDE ---
        self.server = None
        self.client = GameClient()
        self.connected_players = [] 
        
        # --- FONTES ---
        self.ui_font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 80)
        self.small_font = pygame.font.SysFont(None, 30)

        # --- CARREGAMENTO DE ASSETS ---
        assets_path = os.path.join("assets", "img")
        
        # 1. Menu
        try:
            self.bg_menu = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "menu_bg.png")).convert(), (WIDTH, HEIGHT))
            self.logo_image = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "logo.png")).convert_alpha(), (400, 150))
            self.logo_rect = self.logo_image.get_rect(center=(WIDTH // 2, 120))
        except FileNotFoundError:
            self.bg_menu = None
            self.logo_image = None

        # 2. Lobby e Retratos
        try:
            self.bg_lobby = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "lobby_bg.png")).convert(), (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_lobby = None

        portrait_size = (150, 150)
        try:
            self.img_knight = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_knight.png")).convert_alpha(), portrait_size)
            self.img_wizard = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_wizard.png")).convert_alpha(), portrait_size)
            self.img_rogue = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_rogue.png")).convert_alpha(), portrait_size)
        except FileNotFoundError:
            self.img_knight = self.create_fallback_image(portrait_size, BLUE)
            self.img_wizard = self.create_fallback_image(portrait_size, (150, 0, 150))
            self.img_rogue = self.create_fallback_image(portrait_size, (50, 50, 50))

        # 3. Assets da Batalha
        try:
            self.bg_battle = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "battle_bg.png")).convert(), (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_battle = None
            
        try:
            self.img_boss = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "boss_dragon.png")).convert_alpha(), (350, 350))
        except FileNotFoundError:
            self.img_boss = self.create_fallback_image((350, 350), (180, 0, 0))

        # --- BOTÕES E UI (MENU E LOBBY) ---
        center_x = (WIDTH // 2)
        
        self.btn_host = Button(center_x - 150, 280, 300, 60, "Criar Partida (Host)", BLUE, HOVER_BLUE, WHITE)
        self.btn_join = Button(center_x - 150, 370, 300, 60, "Entrar em Partida", BLUE, HOVER_BLUE, WHITE)

        portrait_y = 350 
        spacing = 250 

        self.rect_knight = self.img_knight.get_rect(center=(center_x - spacing, portrait_y))
        self.rect_wizard = self.img_wizard.get_rect(center=(center_x, portrait_y))
        self.rect_rogue = self.img_rogue.get_rect(center=(center_x + spacing, portrait_y))

        self.input_name = TextBox(center_x - 150, 150, 300, 50, WHITE, LIGHT_GREY, BLUE)
        self.btn_start = Button(center_x - 150, 650, 300, 60, "CONECTAR À SALA", BLUE, HOVER_BLUE, WHITE)
        self.btn_start_game = Button(center_x - 150, 650, 300, 60, "INICIAR BATALHA", BLUE, HOVER_BLUE, WHITE)

        # --- BOTÕES DE DESAFIO (BATALHA) ---
        btn_w, btn_h = 350, 40 
        start_x = 420
        start_y = HEIGHT - 130
        
        self.btn_opt_a = Button(start_x, start_y, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)
        self.btn_opt_b = Button(start_x + 370, start_y, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)
        self.btn_opt_c = Button(start_x, start_y + 50, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)
        self.btn_opt_d = Button(start_x + 370, start_y + 50, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)

        # --- SISTEMA DE COMBATE ---
        self.fase_atual = "Pilha" # Define qual banco de perguntas acessar
        self.active_question = None
        self.carregar_nova_pergunta()

    def carregar_nova_pergunta(self):
        """Sorteia uma pergunta e atualiza os botões da tela."""
        self.active_question = get_random_question(self.fase_atual)
        
        # Atualiza os textos dos botões
        self.btn_opt_a.text = self.active_question["opcoes"][0]
        self.btn_opt_b.text = self.active_question["opcoes"][1]
        self.btn_opt_c.text = self.active_question["opcoes"][2]
        self.btn_opt_d.text = self.active_question["opcoes"][3]

    def create_fallback_image(self, size, color):
        fallback = pygame.Surface(size)
        fallback.fill(color)
        return fallback

    def draw_outline(self, image, rect, color, thickness=3):
        mask = pygame.mask.from_surface(image)
        outline = mask.outline()
        if not outline: return
        outline_points = [(p[0] + rect.x, p[1] + rect.y) for p in outline]
        pygame.draw.lines(self.screen, color, True, outline_points, thickness)

    def draw_health_bar(self, x, y, w, h, current_hp, max_hp, color):
        pygame.draw.rect(self.screen, DARK_GREY, (x, y, w, h)) 
        ratio = current_hp / max_hp
        pygame.draw.rect(self.screen, color, (x, y, int(w * ratio), h)) 
        pygame.draw.rect(self.screen, WHITE, (x, y, w, h), 2) 

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            if self.state == "MENU":
                if self.btn_host.is_clicked(event):
                    self.is_host = True
                    self.state = "LOBBY"
                if self.btn_join.is_clicked(event):
                    self.is_host = False
                    self.state = "LOBBY"

            elif self.state == "LOBBY":
                self.input_name.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_knight.collidepoint(event.pos): self.player_class = "Knight"
                    elif self.rect_wizard.collidepoint(event.pos): self.player_class = "Wizard"
                    elif self.rect_rogue.collidepoint(event.pos): self.player_class = "Rogue"
                    
                if self.btn_start.is_clicked(event):
                    self.player_name = self.input_name.text.strip()
                    if self.player_name != "" and self.player_class is not None:
                        if self.is_host:
                            self.server = GameServer()
                            server_thread = threading.Thread(target=self.server.start)
                            server_thread.daemon = True 
                            server_thread.start()

                        if self.client.connect(SERVER_IP):
                            self.client.send_data({"type": "join", "name": self.player_name, "class": self.player_class})
                            self.state = "WAITING_ROOM"
                    else:
                        print("[AVISO] Preencha seu nome e selecione uma classe!")

            elif self.state == "WAITING_ROOM":
                if self.is_host and self.btn_start_game.is_clicked(event):
                    self.client.send_data({"type": "start_game"})
                    self.state = "BATTLE" # Fallback para testes offline

            elif self.state == "BATTLE":
                if self.active_question:
                    correta = self.active_question["correta"]
                    
                    if self.btn_opt_a.is_clicked(event):
                        if correta == 0: print("[ACERTOU] Você causou dano no Boss!")
                        else: print("[ERROU] Você sofreu dano!")
                        self.carregar_nova_pergunta()
                        
                    elif self.btn_opt_b.is_clicked(event):
                        if correta == 1: print("[ACERTOU] Você causou dano no Boss!")
                        else: print("[ERROU] Você sofreu dano!")
                        self.carregar_nova_pergunta()
                        
                    elif self.btn_opt_c.is_clicked(event):
                        if correta == 2: print("[ACERTOU] Você causou dano no Boss!")
                        else: print("[ERROU] Você sofreu dano!")
                        self.carregar_nova_pergunta()
                        
                    elif self.btn_opt_d.is_clicked(event):
                        if correta == 3: print("[ACERTOU] Você causou dano no Boss!")
                        else: print("[ERROU] Você sofreu dano!")
                        self.carregar_nova_pergunta()

    def update(self):
        if self.state == "WAITING_ROOM":
            messages = self.client.get_messages()
            for msg in messages:
                if msg.get("type") == "lobby_update":
                    self.connected_players = msg.get("players", [])
                elif msg.get("type") == "game_start":
                    self.state = "BATTLE"

    def draw_menu(self):
        if self.logo_image: self.screen.blit(self.logo_image, self.logo_rect)
        else: 
            title_surface = self.title_font.render("CODEQUEST", True, WHITE)
            self.screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 120)))
        self.btn_host.draw(self.screen)
        self.btn_join.draw(self.screen)

    def draw_lobby(self):
        if self.bg_lobby: self.screen.blit(self.bg_lobby, (0, 0))
        else: self.screen.fill(DARK_GREY)
        
        title_surf = self.ui_font.render("Configuração de Personagem", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 80)))
        name_label = self.ui_font.render("Seu Nome:", True, WHITE)
        self.screen.blit(name_label, (WIDTH // 2 - 150, 120))
        
        self.input_name.draw(self.screen)
        
        self.screen.blit(self.img_knight, self.rect_knight.topleft)
        self.screen.blit(self.img_wizard, self.rect_wizard.topleft)
        self.screen.blit(self.img_rogue, self.rect_rogue.topleft)

        if self.player_class == "Knight": self.draw_outline(self.img_knight, self.rect_knight, WHITE, 4)
        elif self.player_class == "Wizard": self.draw_outline(self.img_wizard, self.rect_wizard, WHITE, 4)
        elif self.player_class == "Rogue": self.draw_outline(self.img_rogue, self.rect_rogue, WHITE, 4)
        
        self.btn_start.draw(self.screen)

    def draw_waiting_room(self):
        if self.bg_lobby: self.screen.blit(self.bg_lobby, (0, 0))
        else: self.screen.fill(DARK_GREY)

        title = self.title_font.render("SALA DE ESPERA", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        list_bg = pygame.Surface((600, 400))
        list_bg.set_alpha(180) 
        list_bg.fill(BLACK)
        self.screen.blit(list_bg, (WIDTH // 2 - 300, 200))

        header = self.ui_font.render(f"Jogadores Conectados: {len(self.connected_players)}/4", True, BLUE)
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, 230)))

        start_y = 300
        for i, player in enumerate(self.connected_players):
            p_text = self.ui_font.render(f"> {player['name']}  ({player['class']})", True, WHITE)
            self.screen.blit(p_text, (WIDTH // 2 - 250, start_y + (i * 45)))

        if self.is_host: self.btn_start_game.draw(self.screen)
        else:
            wait_text = self.ui_font.render("Aguardando o Host iniciar a batalha...", True, LIGHT_GREY)
            self.screen.blit(wait_text, wait_text.get_rect(center=(WIDTH // 2, 680)))

    def draw_battle(self):
        if self.bg_battle: self.screen.blit(self.bg_battle, (0, 0))
        else: self.screen.fill(BLACK)

        boss_rect = self.img_boss.get_rect(center=(WIDTH - 250, HEIGHT // 2 - 50))
        self.screen.blit(self.img_boss, boss_rect.topleft)
        
        boss_name = self.ui_font.render("Dragão da Pilha", True, (255, 100, 100))
        self.screen.blit(boss_name, (WIDTH - 350, 50))
        self.draw_health_bar(WIDTH - 350, 90, 300, 25, 1000, 1000, (200, 0, 0)) 

        players_to_draw = self.connected_players if self.connected_players else [{"name": self.player_name, "class": self.player_class}]
        players_to_draw = players_to_draw[:5]
        num_players = len(players_to_draw)

        available_height = HEIGHT - 200 
        sprite_size = 110 
        
        spacing = (available_height - (num_players * sprite_size)) // (num_players + 1)
        
        for i, player in enumerate(players_to_draw):
            p_class = player.get("class")
            p_name = player.get("name")
            
            p_img = self.img_knight
            if p_class == "Wizard": p_img = self.img_wizard
            elif p_class == "Rogue": p_img = self.img_rogue
            
            p_battle_img = pygame.transform.scale(p_img, (sprite_size, sprite_size))
            
            pos_y = spacing + i * (sprite_size + spacing)
            p_rect = p_battle_img.get_rect(topleft=(100, pos_y))
            
            self.screen.blit(p_battle_img, p_rect.topleft)
            
            name_surf = self.small_font.render(p_name, True, WHITE)
            name_rect = name_surf.get_rect(center=(p_rect.centerx, p_rect.bottom + 12))
            self.screen.blit(name_surf, name_rect)

        hud_bg = pygame.Surface((WIDTH, 200))
        hud_bg.set_alpha(200)
        hud_bg.fill(DARK_GREY)
        self.screen.blit(hud_bg, (0, HEIGHT - 200))

        name_txt = self.ui_font.render(f"{self.player_name} ({self.player_class})", True, WHITE)
        self.screen.blit(name_txt, (50, HEIGHT - 180))
        
        hp_label = self.small_font.render("HP", True, WHITE)
        self.screen.blit(hp_label, (15, HEIGHT - 130))
        self.draw_health_bar(50, HEIGHT - 130, 250, 20, 100, 100, (0, 200, 0))
        
        mp_label = self.small_font.render("MP", True, WHITE)
        self.screen.blit(mp_label, (15, HEIGHT - 90))
        self.draw_health_bar(50, HEIGHT - 90, 200, 15, 50, 50, (0, 100, 255))

        pygame.draw.rect(self.screen, BLACK, (400, HEIGHT - 180, 750, 160), border_radius=10)
        pygame.draw.rect(self.screen, BLUE, (400, HEIGHT - 180, 750, 160), 3, border_radius=10)
        
        pergunta_texto = self.active_question["pergunta"] if self.active_question else "Carregando..."
        question_surf = self.small_font.render(pergunta_texto, True, WHITE)
        self.screen.blit(question_surf, (420, HEIGHT - 165))

        self.btn_opt_a.draw(self.screen)
        self.btn_opt_b.draw(self.screen)
        self.btn_opt_c.draw(self.screen)
        self.btn_opt_d.draw(self.screen)

    def draw(self):
        if self.state == "MENU":
            if self.bg_menu: self.screen.blit(self.bg_menu, (0, 0))
            else: self.screen.fill(DARK_GREY)
            self.draw_menu()
        elif self.state == "LOBBY": self.draw_lobby()
        elif self.state == "WAITING_ROOM": self.draw_waiting_room()
        elif self.state == "BATTLE": self.draw_battle()
            
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
        if self.client.connected: self.client.disconnect()
        pygame.quit()
        sys.exit()