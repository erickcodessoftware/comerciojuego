from manejador_csv import leer_csv, escribir_csv
from sistema_transporte import SistemaTransporte
from mercado_dinamico import Mercado
from inventario_jugador import Jugador
import os

CIUDADES = ["Ciudad almeja", "Ciudad gotica", "Mordor", "Los santos", "Tecate"]
RECURSOS = ["pan", "agua", "espadas", "escudos", "pocimas"]
RECURSOS_PESOS = {
    "pan": 1,
    "agua": 2,
    "espadas": 5,
    "escudos": 7,
    "pocimas": 3,
}

def mostrar_menu_principal():
    # Limpiar pantalla
    # if os.name == 'nt':  # Windows
    #     os.system('cls')
    print("\n=== Simulador de Comercio ===")
    print("1. Seleccionar jugador")
    print("2. Crear nuevo jugador")
    print("3. Salir")
    return input("Elige una opción: ")

def seleccionar_jugador(jugadores):
    # Limpiar pantalla
    if os.name == 'nt':  # Windows
        os.system('cls')
    print("\n=== Jugadores Disponibles ===")
    for idx, jugador in enumerate(jugadores):
        print(f"{idx + 1}. {jugador.nombre} (Ubicacion: {jugador.ciudad}, Saldo: {jugador.balance} sheintavos)")  # Acceder a los atributos
    print(f"{len(jugadores) + 1}. Regresar al menú principal")
    opcion = int(input("Selecciona un jugador: "))
    if opcion <= len(jugadores):
        jugador = jugadores[opcion - 1]
        return jugador
    return None

def crear_nuevo_jugador(jugadores_csv):
    # Limpiar pantalla
    if os.name == 'nt':  # Windows
        os.system('cls')
    
    nombre = input("\nIngresa tu nombre: ")
    print("Ciudades disponibles: " + ", ".join(CIUDADES))
    ciudad = input("Elige tu ciudad inicial: ")
    
    while ciudad not in CIUDADES:
        print("Ciudad no válida. Intenta de nuevo.")
        ciudad = input("Elige tu ciudad inicial: ")
    
    # Crear el jugador como instancia de la clase Jugador
    jugador = Jugador(nombre)
    jugador.ciudad = ciudad
    jugador.balance = 100  # Saldo inicial en sheintavos

    # Convertir el jugador a un diccionario
    jugador_data = {
        "nombre": jugador.nombre,
        "ciudad": jugador.ciudad,
        "balance": jugador.balance
    }
    
    # Escribir todos los jugadores (nuevos y existentes) en el archivo CSV
    jugadores_csv.append(jugador_data)  # Agregar solo el diccionario
    escribir_csv("datos/jugadores.csv", ["nombre", "ciudad", "balance"], jugadores_csv)

    print(f"¡Jugador {nombre} creado con éxito!")
    return jugador

def cargar_jugadores_csv(jugadores_csv):
    jugadores = []
    for jugador_data in jugadores_csv:
        jugador = Jugador(jugador_data["nombre"])
        jugador.ciudad = jugador_data["ciudad"]
        jugador.balance = int(jugador_data["balance"])  # Asegúrate de que el balance sea un número
        jugadores.append(jugador)
    return jugadores

def obtener_datos_jugadores(jugadores):
    jugadores_csv = []
    for jugador in jugadores:
        # Convertir cada jugador a un diccionario
        jugador_data = {
            "nombre": jugador.nombre,
            "ciudad": jugador.ciudad,
            "balance": jugador.balance
        }
        jugadores_csv.append(jugador_data)
    return jugadores_csv

def mover_jugador(jugador, transporte):
    # Limpiar pantalla
    if os.name == 'nt':  # Windows
        os.system('cls')
    print("\n=== Movimiento entre Ciudades ===")
    print(f"Ciudad actual: {jugador.ciudad}")
    print("Ciudades disponibles para moverse:")
    for ciudad, costo in transporte.ciudades[jugador.ciudad].vecinos.items():
        print(f"- {ciudad} (Costo: {costo} sheintavos)")

    destino = input("Elige una ciudad para moverte: ")
    
    # Verifica si el destino está disponible
    if destino not in transporte.ciudades:
        print("Ciudad no válida. Intenta de nuevo.")
        return jugador

    # Calcular la ruta más corta usando Dijkstra
    ruta_optima, costo_total = transporte.encontrar_ruta_optima(jugador.ciudad, destino)
    
    # Mostrar la ruta más corta y el costo total
    print(f"\nRuta más corta y barata: {' -> '.join(ruta_optima)}")
    print(f"El costo total del viaje es {costo_total} sheintavos.")
    
    # Verificar si el jugador tiene suficiente dinero
    if jugador.balance >= costo_total:
        jugador.ciudad = destino
        jugador.balance -= costo_total
        print(f"Te has movido a {destino}. Tu saldo actual es {jugador.balance} sheintavos.")
    else:
        print("No tienes suficientes sheintavos para moverte.")
    
    return jugador

def comerciar(jugador, mercado):
    # Limpiar pantalla
    if os.name == 'nt':  # Windows
        os.system('cls')
    print("\n=== Comercio ===")
    ciudad = jugador.ciudad
    print(f"Ciudad actual: {ciudad}")
    print(f"Saldo actual: {jugador.balance} sheintavos")
    print("Precios actuales de los recursos:")
    for recurso in RECURSOS:
        print(f"- {recurso}: {mercado.precios[recurso]} sheintavos")
    
    # print("\n1. Comprar recursos (Optimizado)")
    print("2. Comprar recursos")  # Opción para compra manual
    print("3. Vender recursos")
    print("4. Regresar")
    opcion = input("Elige una opción: ")

    # if opcion == "1":
    #     # Llamar a la función para optimizar la compra de recursos
    #     jugador.comerciar(RECURSOS_PESOS, mercado.precios, max_valor=jugador.balance)
    #     print("Compra optimizada realizada.")
    
    if opcion == "2":
        # Compra manual
        recurso = input("¿Qué recurso quieres comprar? ")
        if recurso not in RECURSOS:
            print("Recurso no válido.")
            return jugador
        cantidad = int(input(f"¿Cuántas unidades de {recurso} quieres comprar? "))
        precio = mercado.precios[recurso]
        costo_total = precio * cantidad
        if jugador.balance >= costo_total:
            jugador.balance -= costo_total
            jugador.inventario[recurso] = jugador.inventario.get(recurso, 0) + cantidad
            print(f"Has comprado {cantidad} unidades de {recurso}.")
        else:
            print("No tienes suficientes sheintavos.")
    
    elif opcion == "3":
        # Venta de recursos
        recurso = input("¿Qué recurso quieres vender? ")
        inventario = jugador.inventario
        if recurso not in inventario or inventario[recurso] <= 0:
            print("No tienes suficientes recursos para vender.")
            return jugador
        cantidad = int(input(f"¿Cuántas unidades de {recurso} quieres vender? "))
        if cantidad > inventario[recurso]:
            print("No tienes tantas unidades para vender.")
            return jugador
        precio = mercado.precios[recurso]
        jugador.balance += precio * cantidad
        jugador.inventario[recurso] -= cantidad
        if jugador.inventario[recurso] == 0:
            del jugador.inventario[recurso]
        print(f"Has vendido {cantidad} unidades de {recurso}.")

    return jugador

def mostrar_inventario(jugador):
    # Limpiar pantalla
    if os.name == 'nt':  # Windows
        os.system('cls')
    print("\n=== Inventario del Jugador ===")
    print(f"Nombre: {jugador.nombre}")
    print(f"Ciudad: {jugador.ciudad}")
    print(f"Saldo: {jugador.balance} sheintavos")

    inventario = jugador.inventario
    print("Inventario:")
    if inventario:
        for recurso, cantidad in inventario.items():
            peso = RECURSOS_PESOS.get(recurso, 0)
            print(f"- {recurso}: {cantidad} unidades (Peso por unidad: {peso})")
    else:
        print("El inventario está vacío.")
    input("\nPresiona Enter para continuar...")

def simular():
    jugadores_csv = leer_csv("datos/jugadores.csv")
    jugadores = cargar_jugadores_csv(jugadores_csv)  # Convertir diccionarios a instancias de Jugador
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
                jugador_actual = seleccionar_jugador(jugadores)
            elif opcion == "2":
                jugador_actual = crear_nuevo_jugador(jugadores)
                # Al guardar el jugador nuevo, aseguramos que sea un objeto, no un diccionario
                # Al guardar el jugador nuevo, aseguramos que solo los campos correctos sean guardados
                jugador_data = {
                    "nombre": jugador_actual.nombre,
                    "ciudad": jugador_actual.ciudad,
                    "balance": jugador_actual.balance
                }
                # Asegúrate de que esta línea no escriba un objeto Jugador, sino un diccionario con los datos correctos
                jugadores_csv.append(jugador_data)
                escribir_csv("datos/jugadores.csv", ["nombre", "ciudad", "balance"], jugadores_csv)

            elif opcion == "3":
                print("Saliendo del juego...")
                break
        else:
            # Limpiar pantalla
            if os.name == 'nt':  # Windows
                os.system('cls')
            print(f"\nJugador actual: {jugador_actual.nombre} en {jugador_actual.ciudad}")
            print("1. Moverte a otra ciudad")
            print("2. Comerciar")
            print("3. Ver inventario")  # Nueva opción
            print("4. Regresar al menú principal")
            accion = input("Elige una acción: ")
            if accion == "1":
                jugador_actual = mover_jugador(jugador_actual, transporte)
            elif accion == "2":
                jugador_actual = comerciar(jugador_actual, mercado)
            elif accion == "3":
                mostrar_inventario(jugador_actual)  # Llama a la nueva función
            elif accion == "4":
                jugador_actual = None

if __name__ == "__main__":
    simular()
