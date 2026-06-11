# ui/textbox.py
import pygame

class TextBox:
    def __init__(self, x, y, width, height, text_color, bg_color, active_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = bg_color
        self.color_active = active_color
        self.color = self.color_inactive
        self.text_color = text_color
        self.text = ""
        self.font = pygame.font.SysFont(None, 40)
        self.active = False

    def handle_event(self, event):
        """Lida com cliques do mouse e digitação do teclado."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Se o usuário clicar dentro do retângulo, ativa a caixa
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Muda a cor se estiver ativo
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Opcional: fazer algo ao apertar Enter
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    # Apaga o último caractere
                    self.text = self.text[:-1]
                else:
                    # Limita o tamanho do nome a 15 caracteres
                    if len(self.text) < 15:
                        self.text += event.unicode

    def draw(self, surface):
        """Desenha a caixa e o texto na tela."""
        # Desenha o fundo da caixa de texto
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        # Renderiza o texto digitado
        text_surface = self.font.render(self.text, True, self.text_color)
        # Centraliza o texto verticalmente e dá um pequeno recuo horizontal (padding)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))