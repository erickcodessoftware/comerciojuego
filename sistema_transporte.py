# /game/simulation/sistema_transporte.py

import heapq

class Ciudad:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # {vecino: costo_transporte}

    def agregar_ruta(self, vecino, costo):
        self.vecinos[vecino] = costo

class SistemaTransporte:
    def __init__(self):
        self.ciudades = {}

    def cargar_rutas(self, datos_rutas):
        """Cargar rutas desde una lista de diccionarios."""
        for ruta in datos_rutas:
            ciudad_a = ruta["Ciudad almeja"]
            ciudad_b = ruta["Ciudad gotica"]
            costo = int(ruta["Costo"])
            self.agregar_ciudad(ciudad_a)
            self.agregar_ciudad(ciudad_b)
            self.agregar_ruta(ciudad_a, ciudad_b, costo)

    def agregar_ciudad(self, nombre_ciudad):
        if nombre_ciudad not in self.ciudades:
            self.ciudades[nombre_ciudad] = Ciudad(nombre_ciudad)

    def agregar_ruta(self, ciudad_a, ciudad_b, costo):
        self.ciudades[ciudad_a].agregar_ruta(ciudad_b, costo)
        self.ciudades[ciudad_b].agregar_ruta(ciudad_a, costo)

    def encontrar_ruta_optima(self, inicio, destino):
        """Dijkstra para encontrar la ruta más corta."""
        distancias = {ciudad: float('inf') for ciudad in self.ciudades}
        previos = {ciudad: None for ciudad in self.ciudades}
        distancias[inicio] = 0
        cola_prioridad = [(0, inicio)]

        while cola_prioridad:
            distancia_actual, ciudad_actual = heapq.heappop(cola_prioridad)

            if distancia_actual > distancias[ciudad_actual]:
                continue

            for vecino, costo in self.ciudades[ciudad_actual].vecinos.items():
                nueva_distancia = distancia_actual + costo

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    previos[vecino] = ciudad_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        ruta, ciudad = [], destino
        while ciudad:
            ruta.append(ciudad)
            ciudad = previos[ciudad]
        return ruta[::-1], distancias[destino]
