from classes.personagem import Personagem

class Knight(Personagem):
    def __init__(self, nome: str):
        super().__init__(nome=nome, hp_maximo=150, mana_maxima=30, ataque_base=15)
        self.classe = "Knight"
        
    def to_dict(self) -> dict:
        data["classe"] = self.classe
        return data