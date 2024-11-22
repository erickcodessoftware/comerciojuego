# /game/simulation/mercado_dinamico.py

# metodo de ordenamiento

from collections import defaultdict
import random

class Mercado:
    def __init__(self):
        self.precios = defaultdict(lambda: 10)
        self.oferta = defaultdict(int)
        self.demanda = defaultdict(int)

    def cargar_mercado(self, datos_mercado):
        """Cargar datos del mercado desde un archivo."""
        for recurso in datos_mercado:
            self.oferta[recurso["Recurso"]] = int(recurso["Oferta"])
            self.demanda[recurso["Recurso"]] = int(recurso["Demanda"])
            self.precios[recurso["Recurso"]] = int(recurso["Precio"])

    def actualizar_precios(self):
        for recurso in self.precios.keys():
            if self.demanda[recurso] > self.oferta[recurso]:
                self.precios[recurso] += 1
            elif self.demanda[recurso] < self.oferta[recurso]:
                self.precios[recurso] = max(1, self.precios[recurso] - 1)

    def generar_evento(self):
        """Evento aleatorio que afecta la oferta o la demanda."""
        recurso = random.choice(list(self.precios.keys()))
        cambio = random.randint(-10, 10)
        if random.choice(["oferta", "demanda"]) == "oferta":
            self.oferta[recurso] = max(0, self.oferta[recurso] + cambio)
        else:
            self.demanda[recurso] = max(0, self.demanda[recurso] + cambio)
