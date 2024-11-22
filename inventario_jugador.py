# /game/simulation/inventario_jugador.py

from collections import defaultdict

class Jugador:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.inventario = defaultdict(int)
        self.capacidad = capacidad
        self.balance = 100

    def comerciar(self, recurso, cantidad, precio, comprando=True):
        if comprando:
            if self.capacidad >= sum(self.inventario.values()) + cantidad:
                costo = cantidad * precio
                if self.balance >= costo:
                    self.balance -= costo
                    self.inventario[recurso] += cantidad
                    return True
        else:
            if self.inventario[recurso] >= cantidad:
                self.balance += cantidad * precio
                self.inventario[recurso] -= cantidad
                return True
        return False
