"""O item de inventario da loja.

Esta classe pertence ao "goblin do canto" no kata original: e a estrutura de
dados compartilhada com o resto do sistema, entao ela permanece intacta.
Nenhuma regra de negocio vive aqui - Item so guarda estado (SRP).
"""


class Item:
    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
