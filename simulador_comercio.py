# /game/simulation/simulacion_comercio.py

from manejador_csv import leer_csv, escribir_csv
from sistema_transporte import SistemaTransporte
from mercado_dinamico import Mercado
from inventario_jugador import Jugador

CIUDADES = ["CiudadA", "CiudadB", "CiudadC", "CiudadD", "CiudadE"]
RECURSOS = ["pan", "agua", "espadas", "escudos", "pocimas"]

def mostrar_menu_principal():
    print("\n=== Simulador de Comercio ===")
    print("1. Seleccionar jugador")
    print("2. Crear nuevo jugador")
    print("3. Salir")
    return input("Elige una opción: ")

def seleccionar_jugador(jugadores):
    print("\n=== Jugadores Disponibles ===")
    for idx, jugador in enumerate(jugadores):
        print(f"{idx + 1}. {jugador['nombre']} (Ciudad: {jugador['ciudad']}, Saldo: {jugador['balance']} sheintavos)")
    print(f"{len(jugadores) + 1}. Regresar al menú principal")
    opcion = int(input("Selecciona un jugador: "))
    if opcion <= len(jugadores):
        jugador = jugadores[opcion - 1]
        # Inicializar inventario como un diccionario vacío si no existe
        jugador["inventario"] = jugador.get("inventario", {})
        return jugador
    return None

def crear_nuevo_jugador(jugadores_csv):
    nombre = input("\nIngresa tu nombre: ")
    print("Ciudades disponibles: " + ", ".join(CIUDADES))
    ciudad = input("Elige tu ciudad inicial: ")
    while ciudad not in CIUDADES:
        print("Ciudad no válida. Intenta de nuevo.")
        ciudad = input("Elige tu ciudad inicial: ")
    jugador = {
        "nombre": nombre,
        "ciudad": ciudad,
        "balance": 100,  # Saldo inicial en sheintavos
        "inventario": {}  # Inventario vacío
    }
    jugadores_csv.append(jugador)
    print(f"¡Jugador {nombre} creado con éxito!")
    return jugador

def mover_jugador(jugador, transporte):
    print("\n=== Movimiento entre Ciudades ===")
    print(f"Ciudad actual: {jugador['ciudad']}")
    print("Ciudades disponibles para moverse:")
    for ciudad, costo in transporte.ciudades[jugador["ciudad"]].vecinos.items():
        print(f"- {ciudad} (Costo: {costo} sheintavos)")

    destino = input("Elige una ciudad para moverte: ")
    
    # Verifica si el destino está disponible
    if destino not in transporte.ciudades:
        print("Ciudad no válida. Intenta de nuevo.")
        return jugador

    # Calcular la ruta más corta usando Dijkstra
    ruta_optima, costo_total = transporte.encontrar_ruta_optima(jugador["ciudad"], destino)
    
    # Mostrar la ruta más corta y el costo total
    print(f"\nRuta más corta y barata: {' -> '.join(ruta_optima)}")
    print(f"El costo total del viaje es {costo_total} sheintavos.")
    
    # Verificar si el jugador tiene suficiente dinero
    if int(jugador["balance"]) >= costo_total:
        jugador["ciudad"] = destino
        jugador["balance"] = int(jugador["balance"]) - costo_total
        print(f"Te has movido a {destino}. Tu saldo actual es {jugador['balance']} sheintavos.")
    else:
        print("No tienes suficientes sheintavos para moverte.")
    
    return jugador

def comerciar(jugador, mercado):
    print("\n=== Comercio ===")
    ciudad = jugador["ciudad"]
    print(f"Ciudad actual: {ciudad}")
    print(f"Saldo actual: {jugador['balance']} sheintavos")
    print("Precios actuales de los recursos:")
    for recurso in RECURSOS:
        print(f"- {recurso}: {mercado.precios[recurso]} sheintavos")
    print("\n1. Comprar recursos")
    print("2. Vender recursos")
    print("3. Regresar")
    opcion = input("Elige una opción: ")
    if opcion == "1":
        recurso = input("¿Qué recurso quieres comprar? ")
        if recurso not in RECURSOS:
            print("Recurso no válido.")
            return jugador
        cantidad = int(input(f"¿Cuántas unidades de {recurso} quieres comprar? "))
        precio = mercado.precios[recurso]
        costo_total = precio * cantidad
        if int(jugador["balance"]) >= costo_total:
            jugador["balance"] = int(jugador["balance"]) - costo_total
            jugador["inventario"][recurso] = jugador["inventario"].get(recurso, 0) + cantidad
            print(f"Has comprado {cantidad} unidades de {recurso}.")
        else:
            print("No tienes suficientes sheintavos.")
    elif opcion == "2":
        recurso = input("¿Qué recurso quieres vender? ")
        inventario = jugador.get("inventario", {})
        if recurso not in inventario or inventario[recurso] <= 0:
            print("No tienes suficientes recursos para vender.")
            return jugador
        cantidad = int(input(f"¿Cuántas unidades de {recurso} quieres vender? "))
        if cantidad > inventario[recurso]:
            print("No tienes tantas unidades para vender.")
            return jugador
        precio = mercado.precios[recurso]
        jugador["balance"] = int(jugador["balance"]) + (precio * cantidad)
        jugador["inventario"][recurso] -= cantidad
        if jugador["inventario"][recurso] == 0:
            del jugador["inventario"][recurso]
        print(f"Has vendido {cantidad} unidades de {recurso}.")
    return jugador

def simular():
    jugadores_csv = leer_csv("datos/jugadores.csv")
    datos_rutas = leer_csv("datos/rutas.csv")
    datos_mercado = leer_csv("datos/mercado.csv")

    transporte = SistemaTransporte()
    transporte.cargar_rutas(datos_rutas)

    mercado = Mercado()
    mercado.cargar_mercado(datos_mercado)

    jugador_actual = None
    while True:
        if not jugador_actual:
            opcion = mostrar_menu_principal()
            if opcion == "1":
                jugador_actual = seleccionar_jugador(jugadores_csv)
            elif opcion == "2":
                jugador_actual = crear_nuevo_jugador(jugadores_csv)
                escribir_csv("datos/jugadores.csv", ["nombre", "ciudad", "balance"], jugadores_csv)
            elif opcion == "3":
                print("Saliendo del juego...")
                break
        else:
            print(f"\nJugador actual: {jugador_actual['nombre']} en {jugador_actual['ciudad']}")
            print("1. Moverte a otra ciudad")
            print("2. Comerciar")
            print("3. Regresar al menú principal")
            accion = input("Elige una acción: ")
            if accion == "1":
                jugador_actual = mover_jugador(jugador_actual, transporte)
            elif accion == "2":
                jugador_actual = comerciar(jugador_actual, mercado)
            elif accion == "3":
                jugador_actual = None

if __name__ == "__main__":
    simular()
