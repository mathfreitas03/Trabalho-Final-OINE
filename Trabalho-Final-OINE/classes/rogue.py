import random
from classes.personagem import Personagem

class Rogue(Personagem):
    def __init__(self, nome: str):
        super().__init__(nome=nome, hp_maximo=100, mana_maxima=80, ataque_base=20)
        self.classe = "Rogue"
        self.chance_critico = 0.25

    def atacar(self) -> int:
        dano_final = self.ataque_base
        if random.random() < self.chance_critico:
            dano_final *= 2
        return dano_final

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["classe"] = self.classe
        return data