# estrategia_comercial.py


# Metodo utilizado En el código proporcionado, utilicé el método de ordenamiento por clave (key sorting) de Python, implementado a través de la función sort() de listas.
# Detalles del método:
# Nombre del método: Ordenamiento por clave personalizada.
# Cómo funciona:
# La lista opciones_venta contiene diccionarios con detalles de cada posible venta (ciudad, recurso, cantidad, ganancia).
# El método sort() organiza la lista en función del valor retornado por una función lambda proporcionada como clave (key).
# Se utiliza la clave ganancia del diccionario para definir el criterio de ordenamiento.
# La opción reverse=True asegura que los elementos se ordenen en orden descendente (mayor ganancia primero).


from collections import defaultdict

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.inventario = defaultdict(int)
        self.balance = 100  # Saldo inicial del jugador

def calcular_mejor_venta(inventario, mercado, ciudad_actual):
    """
    Calcula las mejores opciones de venta disponibles en base al inventario
    del jugador, el mercado y la ciudad actual.
    
    Args:
        inventario (dict): Recursos y cantidades que el jugador posee.
        mercado (dict): Información de precios de recursos en distintas ciudades.
        ciudad_actual (str): La ciudad donde se encuentra el jugador.
    
    Returns:
        list: Opciones de venta ordenadas por ganancia (de mayor a menor).
    """
    opciones_venta = []

    for recurso, cantidad in inventario.items():
        # Si no hay suficiente cantidad para vender, omitir este recurso
        if cantidad <= 0:
            continue
        
        for ciudad, precios in mercado.items():
            if recurso in precios:  # Ya no es necesario comparar con ciudad_actual
                precio_venta = precios[recurso]
                ganancia = precio_venta * cantidad
                opciones_venta.append({
                    "ciudad": ciudad,
                    "recurso": recurso,
                    "cantidad": cantidad,
                    "ganancia": ganancia
                })


    # Ordenar las opciones de venta por ganancia de mayor a menor
    opciones_venta.sort(key=lambda x: x["ganancia"], reverse=True)

    return opciones_venta