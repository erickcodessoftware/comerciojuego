# /game/simulation/mercado_dinamico.py

# metodo de ordenamiento

from collections import defaultdict
import random
from config import CIUDADES

class Mercado:
    def __init__(self):
        # Precios por ciudad y recurso
        self.precios_por_ciudad = defaultdict(lambda: defaultdict(lambda: 10))
        self.oferta_por_ciudad = defaultdict(lambda: defaultdict(int))
        self.demanda_por_ciudad = defaultdict(lambda: defaultdict(int))

    def cargar_mercado(self, datos_mercado):
        """Cargar datos del mercado desde un archivo."""
        for recurso in datos_mercado:
            for ciudad in CIUDADES:
                self.oferta_por_ciudad[ciudad][recurso["Recurso"]] = int(recurso["Oferta"])
                self.demanda_por_ciudad[ciudad][recurso["Recurso"]] = int(recurso["Demanda"])
                self.precios_por_ciudad[ciudad][recurso["Recurso"]] = int(recurso["Precio"])

    def actualizar_precios(self, ciudad, recurso, cantidad_comprada_vendida):
        """Actualizar precio de un recurso solo en la ciudad y recurso afectado."""
        if cantidad_comprada_vendida > 0:
            self.precios_por_ciudad[ciudad][recurso] += 1
        elif cantidad_comprada_vendida < 0:
            self.precios_por_ciudad[ciudad][recurso] = max(1, self.precios_por_ciudad[ciudad][recurso] - 1)

    def generar_evento(self):
        """Evento aleatorio que afecta la oferta o la demanda en alguna ciudad."""
        ciudad = random.choice(CIUDADES)
        recurso = random.choice(list(self.precios_por_ciudad[ciudad].keys()))
        cambio = random.randint(-10, 10)
        
        if random.choice(["oferta", "demanda"]) == "oferta":
            self.oferta_por_ciudad[ciudad][recurso] = max(0, self.oferta_por_ciudad[ciudad][recurso] + cambio)
        else:
            self.demanda_por_ciudad[ciudad][recurso] = max(0, self.demanda_por_ciudad[ciudad][recurso] + cambio)




