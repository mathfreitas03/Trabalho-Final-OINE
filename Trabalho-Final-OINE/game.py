# game.py
import pygame
import sys
import os
import threading
import random 

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
        
        # --- INFORMAÇÕES DAS CLASSES ---
        self.class_info = {
            "Knight": {
                "desc": "Um guerreiro robusto da linha de frente.",
                "skill": "Habilidade Overclock: Aumenta em o dano de todos os ataques básicos da equipe."
            },
            "Rogue": {
                "desc": "Furtivo e letal. Especialista em encontrar brechas.",
                "skill": "Habilidade Backdoor: Causa dano massivo direto ao Boss."
            },
            "Wizard": {
                "desc": "Mestre dos códigos e scripts complexos.",
                "skill": "Habilidade DDoS: Sobrecarrega o Boss, paralisando-o por 1 turno."
            },
            "Healer": {
                "desc": "Suporte vital para manter o sistema rodando.",
                "skill": "Habilidade Desfragmentar: Restaura o HP de todos os jogadores da equipe."
            },
            "Bard": {
                "desc": "O animador da equipe. Traz café e boas vibes.",
                "skill": "Habilidade Water Cooler: Toca uma música que restaura o MP de todos os jogadores."
            }
        }
        
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
        
        try:
            self.bg_menu = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "menu_bg.png")).convert(), (WIDTH, HEIGHT))
            self.logo_image = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "logo.png")).convert_alpha(), (600, 225))
            self.logo_rect = self.logo_image.get_rect(center=(WIDTH // 2, 180))
        except FileNotFoundError:
            self.bg_menu = None
            self.logo_image = None

        try:
            self.bg_lobby = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "lobby_bg.png")).convert(), (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_lobby = None

        portrait_size = (150, 150)
        try:
            self.img_knight = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_knight.png")).convert_alpha(), portrait_size)
            self.img_wizard = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_wizard.png")).convert_alpha(), portrait_size)
            self.img_rogue = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_rogue.png")).convert_alpha(), portrait_size)
            self.img_healer = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_healer.png")).convert_alpha(), portrait_size)
            self.img_bard = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "portrait_bard.png")).convert_alpha(), portrait_size)
        except FileNotFoundError:
            self.img_knight = self.create_fallback_image(portrait_size, BLUE)
            self.img_wizard = self.create_fallback_image(portrait_size, (150, 0, 150))
            self.img_rogue = self.create_fallback_image(portrait_size, (50, 50, 50))
            self.img_healer = self.create_fallback_image(portrait_size, (0, 200, 0)) 
            self.img_bard = self.create_fallback_image(portrait_size, (200, 200, 0)) 

        # Cenários de Batalha 
        try:
            self.bg_battle_1 = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "battle_bg.png")).convert(), (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_battle_1 = None
            
        try:
            self.bg_battle_2 = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "battle_bg2.png")).convert(), (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_battle_2 = None
            
        try:
            self.bg_battle_3 = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "battle_bg3.png")).convert(), (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_battle_3 = None
            
        # Sprites dos Inimigos
        try:
            self.img_dragon = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "boss_dragon.png")).convert_alpha(), (350, 350))
        except FileNotFoundError:
            self.img_dragon = self.create_fallback_image((350, 350), (180, 0, 0)) 
            
        try:
            self.img_golem = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "boss_golem.png")).convert_alpha(), (350, 350))
        except FileNotFoundError:
            self.img_golem = self.create_fallback_image((350, 350), (100, 100, 100)) 
            
        try:
            self.img_shaman = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "boss_shaman.png")).convert_alpha(), (350, 350))
        except FileNotFoundError:
            self.img_shaman = self.create_fallback_image((350, 350), (128, 0, 128)) 
            
        try:
            self.img_minion = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "minion_boss.png")).convert_alpha(), (150, 150))
        except FileNotFoundError:
            self.img_minion = self.create_fallback_image((150, 150), (0, 128, 128)) 

        # --- BOTÕES E UI (MENU E LOBBY) ---
        center_x = (WIDTH // 2)
        
        self.btn_host = Button(center_x - 150, 400, 300, 60, "Criar Partida (Host)", BLUE, HOVER_BLUE, WHITE)
        self.btn_join = Button(center_x - 150, 490, 300, 60, "Entrar em Partida", BLUE, HOVER_BLUE, WHITE)

        self.portrait_y = 450 
        spacing = 180 
        
        self.rect_knight = self.img_knight.get_rect(center=(center_x - 2 * spacing, self.portrait_y))
        self.rect_wizard = self.img_wizard.get_rect(center=(center_x - spacing, self.portrait_y))
        self.rect_rogue = self.img_rogue.get_rect(center=(center_x, self.portrait_y))
        self.rect_healer = self.img_healer.get_rect(center=(center_x + spacing, self.portrait_y))
        self.rect_bard = self.img_bard.get_rect(center=(center_x + 2 * spacing, self.portrait_y))

        self.input_name = TextBox(center_x - 150, 150, 300, 50, WHITE, LIGHT_GREY, BLUE)
        self.btn_start = Button(center_x - 150, 650, 300, 60, "CONECTAR À SALA", BLUE, HOVER_BLUE, WHITE)
        self.btn_start_game = Button(center_x - 150, 650, 300, 60, "INICIAR BATALHA", BLUE, HOVER_BLUE, WHITE)

        # --- BOTÕES DE DESAFIO (BATALHA E TURNOS) ---
        btn_w, btn_h = 350, 40 
        start_x = 420
        start_y = HEIGHT - 130
        
        self.btn_attack = Button(start_x, start_y, btn_w, btn_h, "Atacar", BLUE, HOVER_BLUE, WHITE)
        self.btn_skill = Button(start_x + 370, start_y, btn_w, btn_h, "Habilidade (20 MP)", BLUE, HOVER_BLUE, WHITE)
        
        self.btn_opt_a = Button(start_x, start_y, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)
        self.btn_opt_b = Button(start_x + 370, start_y, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)
        self.btn_opt_c = Button(start_x, start_y + 50, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)
        self.btn_opt_d = Button(start_x + 370, start_y + 50, btn_w, btn_h, "", BLUE, HOVER_BLUE, WHITE)
        
        self.btn_continue = Button(0, 0, 300, 40, "Avançar", BLUE, HOVER_BLUE, WHITE)
        self.btn_restart = Button(center_x - 150, 500, 300, 60, "VOLTAR AO MENU", BLUE, HOVER_BLUE, WHITE)
        self.btn_next_level = Button(center_x - 150, 500, 300, 60, "PRÓXIMO BOSS", BLUE, HOVER_BLUE, WHITE)

        # --- SISTEMA DE NÍVEIS E PROGRESSÃO ---
        self.active_question = None
        
        self.player_max_hp = 100
        self.player_hp = 100
        self.player_max_mp = 50
        self.player_mp = 50
        self.skill_cooldown = 0
        
        self.team = [] 
        self.minions = []
        
        self.shaman_stunned = False
        self.boss_stunned = False
        self.attack_multiplier = 1.0 
        self.boss_damage_mult = 1.0 
        
        self.current_turn_idx = -1 
        self.battle_substate = "WAITING_OTHER" 
        self.current_action = None 
        self.battle_message = "" 
        
        self.levels = [
            {"fase": "Pilha", "nome": "Dragão da Pilha", "img": self.img_dragon, "bg": self.bg_battle_1},
            {"fase": "Fila", "nome": "Golem da Fila", "img": self.img_golem, "bg": self.bg_battle_2},
            {"fase": "Arvore", "nome": "Shaman das Árvores", "img": self.img_shaman, "bg": self.bg_battle_3} 
        ]
        
        self.current_level_idx = 0 
        
    def load_level(self):
        level_data = self.levels[self.current_level_idx]
        
        self.fase_atual = level_data["fase"]
        self.boss_name = level_data["nome"]
        self.img_boss = level_data["img"]
        self.current_bg = level_data["bg"] 
        
        self.player_hp = self.player_max_hp 
        self.player_mp = self.player_max_mp 
        self.skill_cooldown = 0
        self.minions = []
        
        # Reset de status
        self.shaman_stunned = False
        self.boss_stunned = False
        self.attack_multiplier = 1.0 
        
        self.team = []
        players_list = self.connected_players if self.connected_players else [{"name": self.player_name, "class": self.player_class}]
        num_players = len(players_list)
        
        # === BALANCEAMENTO MATEMÁTICO ===
        # Batalha 1 e 2 devem durar entre 4 a 6 turnos. Batalha final dura ~8 turnos.
        if self.boss_name == "Dragão da Pilha":
            self.boss_max_hp = num_players * 250
        elif self.boss_name == "Golem da Fila":
            self.boss_max_hp = num_players * 300
        elif self.boss_name == "Shaman das Árvores":
            self.boss_max_hp = num_players * 450
            
        self.boss_hp = self.boss_max_hp
        self.boss_damage_mult = 1.0 + (num_players - 1) * 0.15 
        
        for p in players_list:
            self.team.append({
                "name": p["name"],
                "class": p["class"],
                "hp": 100,
                "max_hp": 100,
                "mp": 50,     
                "max_mp": 50
            })
            
        if self.player_name != "":
            if self.is_host:
                if self.boss_name == "Shaman das Árvores":
                    self.current_turn_idx = len(self.team) - 1 
                else:
                    self.current_turn_idx = -1
                    
                self.start_next_turn()
            else:
                self.battle_substate = "WAITING_OTHER"

    def start_next_turn(self):
        if not self.is_host: 
            return
            
        self.current_turn_idx += 1
        
        while self.current_turn_idx < len(self.team) and self.team[self.current_turn_idx]["hp"] <= 0:
            self.current_turn_idx += 1
            
        if self.current_turn_idx >= len(self.team):
            if self.boss_hp > 0:
                self.execute_boss_turn()
        else:
            self.client.send_data({
                "type": "set_turn",
                "turn_idx": self.current_turn_idx
            })
            self.apply_turn(self.current_turn_idx)

    def apply_turn(self, turn_idx):
        self.current_turn_idx = turn_idx
        current_player = self.team[self.current_turn_idx]
        
        if current_player["name"] == self.player_name:
            if self.player_hp > 0:
                # Diminui o tempo de espera do Cooldown a cada início de turno
                if self.skill_cooldown > 0:
                    self.skill_cooldown -= 1
                    
                self.battle_substate = "ACTION_SELECT"
            else:
                self.client.send_data({"type": "turn_ended"})
                self.battle_substate = "WAITING_OTHER"
        else:
            self.battle_substate = "WAITING_OTHER"

    def carregar_nova_pergunta(self):
        self.active_question = get_random_question(self.fase_atual)
        self.btn_opt_a.text = self.active_question["opcoes"][0]
        self.btn_opt_b.text = self.active_question["opcoes"][1]
        self.btn_opt_c.text = self.active_question["opcoes"][2]
        self.btn_opt_d.text = self.active_question["opcoes"][3]

    def verificar_fim_de_jogo(self):
        if self.boss_hp <= 0:
            self.boss_hp = 0
            if self.current_level_idx < len(self.levels) - 1:
                self.state = "LEVEL_CLEAR"
            else:
                self.state = "VICTORY"
        else:
            if len(self.team) > 0:
                todos_mortos = True
                for p in self.team:
                    if p["hp"] > 0:
                        todos_mortos = False
                        break
                
                if todos_mortos:
                    self.state = "GAME_OVER"

    def execute_player_action(self):
        dano = 0
        cura_grupo = 0
        mp_grupo = 0
        msg_base = ""
        
        if self.current_action == "Attack":
            dano = int(50 * self.attack_multiplier)
            msg_base = f"Resposta Correta! Ataque causou {dano} de dano."
            
        elif self.current_action == "Skill":
            self.player_mp -= 20
            self.skill_cooldown = 2 # Ativa o tempo de espera (2 turnos até poder usar novamente)
            
            for p in self.team:
                if p["name"] == self.player_name:
                    p["mp"] = self.player_mp
            
            if self.player_class == "Knight":
                self.attack_multiplier = 1.5
                msg_base = f"Overclock ativado! Todos os ataques básicos agora dão 1.5x de dano!"
            elif self.player_class == "Rogue":
                dano = 150
                msg_base = f"Backdoor executado! Dano massivo de {dano} direto no Boss!"
            elif self.player_class == "Wizard":
                self.boss_stunned = True
                msg_base = f"DDoS injetado! O Boss foi paralisado por 1 turno!"
            elif self.player_class == "Healer":
                cura_grupo = 40
                msg_base = f"Desfragmentar! Toda a equipe foi curada em {cura_grupo} HP."
            elif self.player_class == "Bard":
                mp_grupo = 30
                msg_base = f"Water Cooler! Toda a equipe recuperou {mp_grupo} MP!"
                
        if cura_grupo > 0 or mp_grupo > 0:
            for p in self.team:
                if p["hp"] > 0:
                    p["hp"] = min(p["max_hp"], p["hp"] + cura_grupo)
                p["mp"] = min(p["max_mp"], p["mp"] + mp_grupo)
                
                if p["name"] == self.player_name:
                    self.player_hp = p["hp"]
                    self.player_mp = p["mp"]

        if dano > 0:
            if self.boss_name == "Shaman das Árvores" and len(self.minions) > 0:
                self.minions[0]["hp"] -= dano
                msg_base += " (Dano absorvido pelo Minion!)"
                
                if self.minions[0]["hp"] <= 0:
                    self.minions.pop(0)
                    msg_base += " Um Minion foi destruído!"
                    
                    if len(self.minions) == 0:
                        self.shaman_stunned = True
                        msg_base += " O Shaman perdeu a proteção e foi atordoado!"
            else:
                self.boss_hp -= dano

        self.battle_message = msg_base

        self.client.send_data({
            "type": "action_result",
            "team": self.team,
            "boss_hp": self.boss_hp,
            "minions": self.minions,
            "shaman_stunned": self.shaman_stunned,
            "boss_stunned": self.boss_stunned,
            "attack_multiplier": self.attack_multiplier,
            "message": self.battle_message
        })

    def processar_resposta(self, opcao_escolhida):
        if self.active_question:
            correta = self.active_question["correta"]
            
            if opcao_escolhida == correta:
                self.execute_player_action()
            else:
                dano_sofrido = 25
                self.player_hp -= dano_sofrido
                for p in self.team:
                    if p["name"] == self.player_name:
                        p["hp"] = self.player_hp
                
                if self.boss_name == "Shaman das Árvores" and len(self.minions) > 0:
                    self.battle_message = f"Incorreto! Os Minions puniram {self.player_name} com {dano_sofrido} de dano!"
                else:
                    self.battle_message = f"Incorreto! O Boss puniu {self.player_name} com {dano_sofrido} de dano!"
                
                if self.player_hp <= 0:
                    self.battle_message += " (Foi ELIMINADO!)"
                    
                self.client.send_data({
                    "type": "action_result",
                    "team": self.team,
                    "boss_hp": self.boss_hp,
                    "minions": self.minions,
                    "shaman_stunned": self.shaman_stunned,
                    "boss_stunned": self.boss_stunned,
                    "attack_multiplier": self.attack_multiplier,
                    "message": self.battle_message
                })
                    
            self.verificar_fim_de_jogo()
            
            if self.state == "BATTLE":
                if self.player_hp <= 0:
                    self.client.send_data({"type": "turn_ended"})
                    self.battle_substate = "WAITING_OTHER"
                else:
                    self.battle_substate = "TURN_RESULT"

    def execute_boss_turn(self):
        if not self.is_host:
            return

        if self.boss_stunned:
            self.battle_message = f"O {self.boss_name} foi paralisado por um DDoS e perdeu o turno!"
            self.boss_stunned = False 
            
            self.client.send_data({
                "type": "boss_action",
                "team": self.team,
                "boss_hp": self.boss_hp,
                "minions": self.minions,
                "shaman_stunned": self.shaman_stunned,
                "boss_stunned": self.boss_stunned,
                "message": self.battle_message
            })
            
            self.verificar_fim_de_jogo()
            if self.state == "BATTLE":
                self.battle_substate = "BOSS_TURN"
            return

        jogadores_vivos = [p for p in self.team if p["hp"] > 0]
        if not jogadores_vivos:
            self.state = "GAME_OVER"
            return
            
        jogadores_em_perigo = [p for p in jogadores_vivos if p["hp"] <= (p["max_hp"] * 0.15)]
        
        if jogadores_em_perigo:
            alvo = min(jogadores_em_perigo, key=lambda x: x["hp"])
            motivo = " (Foco no alvo ferido!)"
        else:
            alvo = random.choice(jogadores_vivos)
            motivo = ""

        acao_boss = random.choices(["Attack", "Special"], weights=[70, 30], k=1)[0]
        
        if self.boss_name == "Shaman das Árvores":
            dano_minion = int(15 * self.boss_damage_mult)
            
            if self.shaman_stunned:
                self.battle_message = "O Shaman está atordoado sem escudo e não pôde agir!"
                self.shaman_stunned = False
            elif len(self.minions) == 0:
                qtd = random.choice([1, 2])
                self.minions = [{"hp": 100, "max_hp": 100} for _ in range(qtd)]
                self.battle_message = f"O Shaman cantou e invocou {qtd} Minion(s)!"
            else:
                minion = random.choice(self.minions)
                if random.random() < 0.20: 
                    minion["hp"] = minion["max_hp"]
                    heal_msg = "Curou TOTALMENTE um minion (Crítico!)"
                else:
                    minion["hp"] = min(minion["max_hp"], minion["hp"] + 20)
                    heal_msg = "Curou 20 HP de um minion"

                atacados = []
                for _ in self.minions:
                    alvo_m = random.choice(jogadores_vivos)
                    alvo_m["hp"] -= dano_minion
                    if alvo_m["hp"] < 0: alvo_m["hp"] = 0
                    if alvo_m["hp"] == 0:
                        atacados.append(f"{alvo_m['name']} (Eliminado!)")
                    else:
                        atacados.append(alvo_m["name"])
                    
                self.battle_message = f"O Shaman {heal_msg}! E os minions atacaram ({dano_minion} DMG): {', '.join(atacados)}."

        elif self.boss_name == "Dragão da Pilha":
            dano_atk = int(20 * self.boss_damage_mult)
            dano_esp = int(45 * self.boss_damage_mult)
            
            if acao_boss == "Attack":
                alvo["hp"] -= dano_atk
                if alvo["hp"] <= 0:
                    self.battle_message = f"O Dragão cuspiu fogo e ELIMINOU {alvo['name']}!{motivo}"
                else:
                    self.battle_message = f"O Dragão cuspiu fogo em {alvo['name']}! {dano_atk} de dano{motivo}"
            else:
                alvo["hp"] -= dano_esp
                if alvo["hp"] <= 0:
                    self.battle_message = f"CUIDADO! O Dragão usou Sopro Infernal e ELIMINOU {alvo['name']}!{motivo}"
                else:
                    self.battle_message = f"CUIDADO! O Dragão usou Sopro Infernal em {alvo['name']}! {dano_esp} de dano{motivo}"
                
        elif self.boss_name == "Golem da Fila":
            dano_atk = int(30 * self.boss_damage_mult)
            dano_esp = int(55 * self.boss_damage_mult)
            
            if acao_boss == "Attack":
                alvo["hp"] -= dano_atk 
                if alvo["hp"] <= 0:
                    self.battle_message = f"O Golem atirou uma rocha e ELIMINOU {alvo['name']}!{motivo}"
                else:
                    self.battle_message = f"O Golem atirou uma rocha em {alvo['name']}! {dano_atk} de dano{motivo}"
            else:
                alvo["hp"] -= dano_esp
                if alvo["hp"] <= 0:
                    self.battle_message = f"CUIDADO! O Terremoto do Golem ELIMINOU {alvo['name']}!{motivo}"
                else:
                    self.battle_message = f"CUIDADO! O Golem causou um Terremoto e atingiu {alvo['name']}! {dano_esp} de dano{motivo}"

        for p in self.team:
            if p["name"] == self.player_name:
                self.player_hp = p["hp"]
            
        self.client.send_data({
            "type": "boss_action",
            "team": self.team,
            "boss_hp": self.boss_hp,
            "minions": self.minions,
            "shaman_stunned": self.shaman_stunned,
            "boss_stunned": self.boss_stunned,
            "message": self.battle_message
        })
            
        self.verificar_fim_de_jogo()
        if self.state == "BATTLE":
            self.battle_substate = "BOSS_TURN"

    def reset_game(self):
        self.current_level_idx = 0 
        self.state = "MENU"

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
        ratio = max(0, current_hp / max_hp)
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
                    elif self.rect_healer.collidepoint(event.pos): self.player_class = "Healer"
                    elif self.rect_bard.collidepoint(event.pos): self.player_class = "Bard"
                    
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

            elif self.state == "BATTLE":
                if self.battle_substate == "ACTION_SELECT":
                    if self.btn_attack.is_clicked(event):
                        self.current_action = "Attack"
                        self.carregar_nova_pergunta()
                        self.battle_substate = "QUESTION"
                        
                    elif self.btn_skill.is_clicked(event):
                        # Validação Dupla de Cooldown e MP
                        if self.skill_cooldown > 0:
                            print(f"[AVISO] Habilidade em Cooldown! Espere {self.skill_cooldown} turnos.")
                        elif self.player_mp >= 20:
                            self.current_action = "Skill"
                            self.execute_player_action()
                            self.verificar_fim_de_jogo()
                            if self.state == "BATTLE":
                                self.battle_substate = "TURN_RESULT"
                        else:
                            print("[AVISO] MP Insuficiente para Habilidade!")
                            
                elif self.battle_substate == "QUESTION":
                    if self.btn_opt_a.is_clicked(event): self.processar_resposta(0)
                    elif self.btn_opt_b.is_clicked(event): self.processar_resposta(1)
                    elif self.btn_opt_c.is_clicked(event): self.processar_resposta(2)
                    elif self.btn_opt_d.is_clicked(event): self.processar_resposta(3)

                elif self.battle_substate == "TURN_RESULT":
                    current_player = self.team[self.current_turn_idx]
                    if current_player["name"] == self.player_name:
                        if self.btn_continue.is_clicked(event):
                            self.client.send_data({"type": "turn_ended"})
                            self.battle_substate = "WAITING_OTHER"

                elif self.battle_substate == "BOSS_TURN":
                    if self.is_host and self.btn_continue.is_clicked(event):
                        self.current_turn_idx = -1
                        self.start_next_turn()

            elif self.state == "LEVEL_CLEAR":
                if self.is_host and self.btn_next_level.is_clicked(event):
                    self.client.send_data({"type": "next_level"})

            elif self.state in ["VICTORY", "GAME_OVER"]:
                if self.btn_restart.is_clicked(event):
                    self.reset_game()

    def update(self):
        messages = self.client.get_messages()
        for msg in messages:
            msg_type = msg.get("type")
            
            if msg_type == "lobby_update":
                self.connected_players = msg.get("players", [])
                
            elif msg_type == "game_start":
                self.load_level()
                self.state = "BATTLE"
                
            elif msg_type == "next_level":
                self.current_level_idx += 1
                self.load_level()
                self.state = "BATTLE"
                
            elif msg_type == "set_turn":
                self.apply_turn(msg.get("turn_idx"))
                
            elif msg_type in ["action_result", "boss_action"]:
                if "attack_multiplier" in msg: self.attack_multiplier = msg.get("attack_multiplier")
                if "boss_stunned" in msg: self.boss_stunned = msg.get("boss_stunned")
                if "shaman_stunned" in msg: self.shaman_stunned = msg.get("shaman_stunned")
                
                if "team" in msg:
                    self.team = msg.get("team")
                    for p in self.team:
                        if p["name"] == self.player_name:
                            self.player_hp = p["hp"]
                            self.player_mp = p["mp"]
                            
                if "boss_hp" in msg: self.boss_hp = msg.get("boss_hp")
                if "minions" in msg: self.minions = msg.get("minions")
                
                self.battle_message = msg.get("message")
                self.verificar_fim_de_jogo()
                
                if self.state == "BATTLE":
                    if msg_type == "action_result":
                        if self.player_hp > 0:
                            self.battle_substate = "TURN_RESULT"
                    else:
                        self.battle_substate = "BOSS_TURN"
                        
            elif msg_type == "turn_ended":
                if self.is_host:
                    self.start_next_turn()

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
        self.screen.blit(self.img_healer, self.rect_healer.topleft)
        self.screen.blit(self.img_bard, self.rect_bard.topleft)

        classes_info = [
            ("Knight", self.rect_knight),
            ("Wizard", self.rect_wizard),
            ("Rogue", self.rect_rogue),
            ("Healer", self.rect_healer),
            ("Bard", self.rect_bard)
        ]
        
        for class_name, rect in classes_info:
            label_surf = self.small_font.render(class_name, True, WHITE)
            label_rect = label_surf.get_rect(center=(rect.centerx, rect.top - 20))
            self.screen.blit(label_surf, label_rect)

        if self.player_class == "Knight": self.draw_outline(self.img_knight, self.rect_knight, WHITE, 4)
        elif self.player_class == "Wizard": self.draw_outline(self.img_wizard, self.rect_wizard, WHITE, 4)
        elif self.player_class == "Rogue": self.draw_outline(self.img_rogue, self.rect_rogue, WHITE, 4)
        elif self.player_class == "Healer": self.draw_outline(self.img_healer, self.rect_healer, WHITE, 4)
        elif self.player_class == "Bard": self.draw_outline(self.img_bard, self.rect_bard, WHITE, 4)
        
        if self.player_class:
            desc_text = self.class_info[self.player_class]["desc"]
            skill_text = self.class_info[self.player_class]["skill"]
            
            desc_surf = self.small_font.render(desc_text, True, WHITE)
            skill_surf = self.small_font.render(skill_text, True, (100, 255, 100))
            
            self.screen.blit(desc_surf, desc_surf.get_rect(center=(WIDTH // 2, self.portrait_y + 110)))
            self.screen.blit(skill_surf, skill_surf.get_rect(center=(WIDTH // 2, self.portrait_y + 140)))

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
        if self.current_bg: self.screen.blit(self.current_bg, (0, 0))
        else: self.screen.fill(BLACK)

        boss_rect = self.img_boss.get_rect(center=(WIDTH - 250, HEIGHT // 2 - 50))
        self.screen.blit(self.img_boss, boss_rect.topleft)
        
        boss_name_surf = self.ui_font.render(self.boss_name, True, (255, 100, 100))
        self.screen.blit(boss_name_surf, (WIDTH - 350, 50))
        
        self.draw_health_bar(WIDTH - 350, 90, 300, 25, self.boss_hp, self.boss_max_hp, (200, 0, 0)) 
        hp_text = self.small_font.render(f"{self.boss_hp}/{self.boss_max_hp}", True, WHITE)
        self.screen.blit(hp_text, (WIDTH - 220, 120))

        if self.boss_name == "Shaman das Árvores" and len(self.minions) > 0:
            start_mx = WIDTH - 450
            start_my = HEIGHT // 2
            for i, m in enumerate(self.minions):
                m_rect = self.img_minion.get_rect(center=(start_mx + (i * 140), start_my + (i * 80)))
                self.screen.blit(self.img_minion, m_rect.topleft)
                self.draw_health_bar(m_rect.x, m_rect.bottom + 5, m_rect.width, 10, m["hp"], m["max_hp"], (255, 100, 0))

        team_to_draw = self.team[:5]
        num_players = len(team_to_draw)

        available_height = HEIGHT - 200 
        sprite_size = 110 
        spacing = (available_height - (num_players * sprite_size)) // (num_players + 1)
        
        for i, p_data in enumerate(team_to_draw):
            p_class = p_data.get("class")
            p_name = p_data.get("name")
            p_hp = p_data.get("hp")
            p_max = p_data.get("max_hp")
            
            p_img = self.img_knight
            if p_class == "Wizard": p_img = self.img_wizard
            elif p_class == "Rogue": p_img = self.img_rogue
            elif p_class == "Healer": p_img = self.img_healer
            elif p_class == "Bard": p_img = self.img_bard
            
            if p_hp <= 0:
                p_img = p_img.copy()
                p_img.set_alpha(80)
            
            p_battle_img = pygame.transform.scale(p_img, (sprite_size, sprite_size))
            pos_y = spacing + i * (sprite_size + spacing)
            p_rect = p_battle_img.get_rect(topleft=(100, pos_y))
            
            self.screen.blit(p_battle_img, p_rect.topleft)
            name_surf = self.small_font.render(p_name, True, WHITE)
            name_rect = name_surf.get_rect(center=(p_rect.centerx, p_rect.bottom + 12))
            self.screen.blit(name_surf, name_rect)
            
            hp_w = 80
            hp_x = p_rect.centerx - (hp_w // 2)
            hp_y = p_rect.bottom + 30
            self.draw_health_bar(hp_x, hp_y, hp_w, 8, p_hp, p_max, (0, 200, 0))
            
            if self.battle_substate not in ["BOSS_TURN", "TURN_RESULT"] and i == self.current_turn_idx:
                turn_indicator = self.small_font.render("<<<", True, (255, 255, 0))
                self.screen.blit(turn_indicator, (p_rect.right + 10, p_rect.centery))

        hud_bg = pygame.Surface((WIDTH, 200))
        hud_bg.set_alpha(200)
        hud_bg.fill(DARK_GREY)
        self.screen.blit(hud_bg, (0, HEIGHT - 200))

        name_txt = self.ui_font.render(f"{self.player_name} ({self.player_class})", True, WHITE)
        self.screen.blit(name_txt, (50, HEIGHT - 180))
        
        hp_label = self.small_font.render("HP", True, WHITE)
        self.screen.blit(hp_label, (15, HEIGHT - 130))
        self.draw_health_bar(50, HEIGHT - 130, 250, 20, self.player_hp, self.player_max_hp, (0, 200, 0))
        
        mp_label = self.small_font.render("MP", True, WHITE)
        self.screen.blit(mp_label, (15, HEIGHT - 90))
        self.draw_health_bar(50, HEIGHT - 90, 200, 15, self.player_mp, self.player_max_mp, (0, 100, 255))

        pygame.draw.rect(self.screen, BLACK, (400, HEIGHT - 180, 750, 160), border_radius=10)
        pygame.draw.rect(self.screen, BLUE, (400, HEIGHT - 180, 750, 160), 3, border_radius=10)
        
        if self.battle_substate == "ACTION_SELECT":
            info_surf = self.ui_font.render("SEU TURNO! Escolha uma ação:", True, WHITE)
            self.screen.blit(info_surf, (420, HEIGHT - 165))
            self.btn_attack.draw(self.screen)
            
            # --- ATUALIZAÇÃO VISUAL DO BOTÃO DE HABILIDADE ---
            if self.skill_cooldown > 0:
                self.btn_skill.text = f"Espera ({self.skill_cooldown} Turno(s))"
                self.btn_skill.color = (80, 80, 80)
                self.btn_skill.hover_color = (80, 80, 80)
            elif self.player_mp < 20:
                self.btn_skill.text = "Sem MP (20 MP)"
                self.btn_skill.color = (80, 80, 80)
                self.btn_skill.hover_color = (80, 80, 80)
            else:
                self.btn_skill.text = "Habilidade (20 MP)"
                self.btn_skill.color = BLUE
                self.btn_skill.hover_color = HOVER_BLUE
                
            self.btn_skill.draw(self.screen)
            
        elif self.battle_substate == "QUESTION":
            pergunta_texto = self.active_question["pergunta"] if self.active_question else "Carregando..."
            question_surf = self.small_font.render(pergunta_texto, True, WHITE)
            self.screen.blit(question_surf, (420, HEIGHT - 165))
            self.btn_opt_a.draw(self.screen)
            self.btn_opt_b.draw(self.screen)
            self.btn_opt_c.draw(self.screen)
            self.btn_opt_d.draw(self.screen)
            
        elif self.battle_substate == "WAITING_OTHER":
            if 0 <= self.current_turn_idx < len(self.team):
                ally_name = self.team[self.current_turn_idx]["name"]
                info_surf = self.ui_font.render(f"Aguardando turno de {ally_name}...", True, LIGHT_GREY)
                self.screen.blit(info_surf, (420, HEIGHT - 165))
            
        elif self.battle_substate == "TURN_RESULT":
            msg_surf = self.small_font.render(self.battle_message, True, WHITE)
            self.screen.blit(msg_surf, msg_surf.get_rect(center=(400 + 750//2, HEIGHT - 130)))
            
            if 0 <= self.current_turn_idx < len(self.team):
                current_player = self.team[self.current_turn_idx]
                if current_player["name"] == self.player_name:
                    self.btn_continue.rect.center = (400 + 750//2, HEIGHT - 60)
                    self.btn_continue.draw(self.screen)
                else:
                    info_surf = self.small_font.render(f"Aguardando {current_player['name']} avançar...", True, LIGHT_GREY)
                    self.screen.blit(info_surf, info_surf.get_rect(center=(400 + 750//2, HEIGHT - 60)))
                
        elif self.battle_substate == "BOSS_TURN":
            msg_surf = self.small_font.render(self.battle_message, True, WHITE)
            self.screen.blit(msg_surf, msg_surf.get_rect(center=(400 + 750//2, HEIGHT - 130)))
            
            if self.is_host:
                self.btn_continue.rect.center = (400 + 750//2, HEIGHT - 60)
                self.btn_continue.draw(self.screen)
            else:
                info_surf = self.small_font.render(f"Aguardando o Host avançar o turno...", True, LIGHT_GREY)
                self.screen.blit(info_surf, info_surf.get_rect(center=(400 + 750//2, HEIGHT - 60)))

    def draw_level_clear(self):
        self.screen.fill(BLACK)
        title = self.title_font.render("BOSS DERROTADO!", True, (50, 255, 50))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        
        sub = self.ui_font.render("O próximo desafio aguarda...", True, WHITE)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        
        if self.is_host:
            self.btn_next_level.draw(self.screen)
        else:
            info_surf = self.small_font.render("Aguardando o Host avançar de fase...", True, LIGHT_GREY)
            self.screen.blit(info_surf, info_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))

    def draw_end_screen(self, title_text, color):
        self.screen.fill(BLACK)
        title = self.title_font.render(title_text, True, color)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        
        if self.state == "VICTORY":
            sub = self.ui_font.render("Você dominou TODAS as Estruturas de Dados!", True, WHITE)
        else:
            sub = self.ui_font.render("O seu grupo foi totalmente aniquilado. Tente novamente.", True, WHITE)
            
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        self.btn_restart.draw(self.screen)

    def draw(self):
        if self.state == "MENU":
            if self.bg_menu: self.screen.blit(self.bg_menu, (0, 0))
            else: self.screen.fill(DARK_GREY)
            self.draw_menu()
        elif self.state == "LOBBY": self.draw_lobby()
        elif self.state == "WAITING_ROOM": self.draw_waiting_room()
        elif self.state == "BATTLE": self.draw_battle()
        elif self.state == "LEVEL_CLEAR": self.draw_level_clear()
        elif self.state == "VICTORY": self.draw_end_screen("VITÓRIA FINAL!", (50, 255, 50))
        elif self.state == "GAME_OVER": self.draw_end_screen("GAME OVER", (255, 50, 50))
            
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