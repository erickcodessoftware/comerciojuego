# /game/simulation/manejador_csv.py

import csv

def leer_csv(ruta_archivo):
    """Leer datos de un archivo CSV y devolver como lista de diccionarios."""
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        return [fila for fila in lector]

def escribir_csv(ruta_archivo, encabezados, datos):
    """Escribir datos en un archivo CSV dado un encabezado y una lista de diccionarios."""
    with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=encabezados)
        escritor.writeheader()
        escritor.writerows(datos)
