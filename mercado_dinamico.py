from collections import defaultdict
import random
from config import CIUDADES

# metodo utilizado

# método de programación dinámica básico basado en memoización, 
# que es una técnica fundamental dentro de la programación dinámica. 
# La idea central de la programación dinámica es almacenar resultados intermedios 
# de cálculos para evitar repetir los mismos cálculos múltiples veces, y la 
# memoización logra esto guardando los resultados en un almacenamiento intermedio (como un diccionario o un cache).

class Mercado:
    def __init__(self):
        # Precios por ciudad y recurso
        self.precios_por_ciudad = defaultdict(lambda: defaultdict(lambda: 10))
        self.oferta_por_ciudad = defaultdict(lambda: defaultdict(int))
        self.demanda_por_ciudad = defaultdict(lambda: defaultdict(int))
        self.memo_precios = {}  # Memoización para precios calculados dinámicamente
        self.memo_oferta_demanda = {}  # Memoización para oferta/demanda

    def cargar_mercado(self, datos_mercado):
        """Cargar datos del mercado desde un archivo."""
        for recurso in datos_mercado:
            for ciudad in CIUDADES:
                self.oferta_por_ciudad[ciudad][recurso["Recurso"]] = int(recurso["Oferta"])
                self.demanda_por_ciudad[ciudad][recurso["Recurso"]] = int(recurso["Demanda"])
                self.precios_por_ciudad[ciudad][recurso["Recurso"]] = int(recurso["Precio"])

    def actualizar_precios(self, ciudad, recurso, cantidad_comprada_vendida):
        """Actualizar precio de un recurso solo en la ciudad y recurso afectado."""
        clave_precio = (ciudad, recurso)
        
        if clave_precio not in self.memo_precios:
            self.memo_precios[clave_precio] = self.precios_por_ciudad[ciudad][recurso]
        
        if cantidad_comprada_vendida > 0:
            self.memo_precios[clave_precio] += 1
        elif cantidad_comprada_vendida < 0:
            self.memo_precios[clave_precio] = max(1, self.memo_precios[clave_precio] - 1)
        
        # Actualizar el precio en el mercado real
        self.precios_por_ciudad[ciudad][recurso] = self.memo_precios[clave_precio]

    def obtener_oferta_demanda(self, ciudad, recurso):
        """Obtener oferta y demanda, usando memoización para evitar cálculos redundantes."""
        clave_oferta_demanda = (ciudad, recurso)
        
        if clave_oferta_demanda not in self.memo_oferta_demanda:
            self.memo_oferta_demanda[clave_oferta_demanda] = {
                "oferta": self.oferta_por_ciudad[ciudad][recurso],
                "demanda": self.demanda_por_ciudad[ciudad][recurso]
            }
        
        return self.memo_oferta_demanda[clave_oferta_demanda]

    def generar_evento(self):
        """Evento aleatorio que afecta la oferta o la demanda en alguna ciudad."""
        ciudad = random.choice(CIUDADES)
        recurso = random.choice(list(self.precios_por_ciudad[ciudad].keys()))
        cambio = random.randint(-10, 10)
        
        if random.choice(["oferta", "demanda"]) == "oferta":
            self.oferta_por_ciudad[ciudad][recurso] = max(0, self.oferta_por_ciudad[ciudad][recurso] + cambio)
        else:
            self.demanda_por_ciudad[ciudad][recurso] = max(0, self.demanda_por_ciudad[ciudad][recurso] + cambio)
        
        # Invalidar memoización relacionada
        clave_oferta_demanda = (ciudad, recurso)
        if clave_oferta_demanda in self.memo_oferta_demanda:
            del self.memo_oferta_demanda[clave_oferta_demanda]
