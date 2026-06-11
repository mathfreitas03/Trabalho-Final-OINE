from classes.personagem import Personagem

class Wizard(Personagem):
    def __init__(self, nome: str):
        super().__init__(nome=nome, hp_maximo=70, mana_maxima=150, ataque_base=30)
        self.classe = "Wizard"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["classe"] = self.classe
        return data