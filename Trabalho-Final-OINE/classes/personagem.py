class Personagem:
    def __init__(self, nome: str, hp_maximo: int, mana_maxima: int, ataque_base: int):
        self.nome = nome
        self.hp_maximo = hp_maximo
        self.hp_atual = hp_maximo
        self.mana_maxima = mana_maxima
        self.mana_atual = mana_maxima
        self.ataque_base = ataque_base
        self.level = 1
        self.xp = 0
        self.is_alive = True

    def receber_dano(self, dano: int) -> None:
        self.hp_atual -= dano
        if self.hp_atual <= 0:
            self.hp_atual = 0
            self.is_alive = False

    def atacar(self) -> int:
        return self.ataque_base

    def adicionar_xp(self, xp_ganho: int) -> None:
        self.xp += xp_ganho

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "hp": self.hp_atual,
            "hp_maximo": self.hp_maximo,
            "mana": self.mana_atual,
            "mana_maxima": self.mana_maxima,
            "level": self.level,
            "vivo": self.is_alive
        }