import csv
from manejador_csv import leer_csv, escribir_csv
from sistema_transporte import SistemaTransporte
from mercado_dinamico import Mercado
from estrategia_comercial import calcular_mejor_venta
from config import CIUDADES
from estrategia_comercial import Jugador
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
    if os.name == 'nt':  # Windows
        os.system('cls')
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

    while True: 
        nombre = input("\nIngresa tu nombre: ")

        # Verificar si el nombre ya existe en la lista de jugadores
        if any(jugador.nombre.lower() == nombre.lower() for jugador in jugadores_csv):
            print(f"El jugador con el nombre '{nombre}' ya existe. Elige otro nombre.")
            input("\nPresiona Enter para continuar...")
        else:
            break 

    print("Ciudades disponibles: " + ", ".join(CIUDADES))
    ciudad = input("Elige tu ciudad inicial: ")
    
    while ciudad not in CIUDADES:
        print("Ciudad no válida. Intenta de nuevo.")
        ciudad = input("Elige tu ciudad inicial: ")
    
    jugador = Jugador(nombre)
    jugador.ciudad = ciudad
    jugador.balance = 100

    # Convertir el jugador a un diccionario
    jugador_data = {
        "nombre": jugador.nombre,
        "ciudad": jugador.ciudad,
        "balance": jugador.balance
    }
    
    with open("datos/jugadores.csv", mode='a', encoding='utf-8', newline='') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "ciudad", "balance"])
        if os.path.getsize("datos/jugadores.csv") == 0:
            escritor.writeheader()
        escritor.writerow(jugador_data)

    print(f"¡Jugador {nombre} creado con éxito!")
    input("\nPresiona Enter para continuar...")
    return jugador


def cargar_jugadores_csv(jugadores_csv):
    jugadores = []
    for jugador_data in jugadores_csv:
        jugador = Jugador(jugador_data["nombre"])
        jugador.ciudad = jugador_data["ciudad"]
        jugador.balance = int(jugador_data["balance"])
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

    # Mostrar todas las ciudades y calcular costos
    print("Ciudades disponibles para moverse:")
    costos_ciudades = {}
    ciudades_lista = []
    
    for index, ciudad in enumerate(transporte.ciudades, start=1):
        if ciudad == jugador.ciudad:
            continue

        # Calcular ruta más corta solo si está conectada directamente, sino aplicar costo base más alto
        if ciudad in transporte.ciudades[jugador.ciudad].vecinos:
            _, costo_base = transporte.encontrar_ruta_optima(jugador.ciudad, ciudad)
        else:
            costo_base = 25  # Precio base más alto para ciudades no conectadas directamente

        costos_ciudades[ciudad] = costo_base
        ciudades_lista.append(ciudad)
        print(f"{index}. {ciudad} (Costo base: {costo_base} sheintavos)")

    # Pedir al usuario que elija una ciudad por número
    try:
        opcion = int(input("\nElige una ciudad para moverte (número): "))
        destino = ciudades_lista[opcion - 1]  # Ajustar para que la selección comience desde 1
    except (ValueError, IndexError):
        print("Ciudad no válida. Intenta de nuevo.")
        input("\nPresiona Enter para continuar...")
        return jugador

    peso_total = 0
    print("\n=== Detalles del Inventario ===")
    for recurso, cantidad in jugador.inventario.items():
        peso_recurso = RECURSOS_PESOS.get(recurso, 0)
        peso_total += cantidad * peso_recurso
        print(f"{recurso}: {cantidad} unidades, {peso_recurso} peso/unidad, Total: {cantidad * peso_recurso} peso")

    print(f"Peso total del inventario: {peso_total} unidades.")
    input("\nPresiona Enter para continuar...")

    # Costo base y cálculo del costo total
    costo_base = costos_ciudades[destino]
    costo_adicional = int(peso_total * 0.8)
    costo_total = costo_base + costo_adicional

    # Mostrar detalles finales del viaje
    print(f"\nCosto base del viaje: {costo_base} sheintavos.")
    print(f"Costo adicional por peso: {costo_adicional} sheintavos.")
    print(f"El costo total del viaje es {costo_total} sheintavos.")
    input("\nPresiona Enter para continuar...")

    # Verificar si el jugador tiene suficiente dinero
    if jugador.balance >= costo_total:
        jugador.ciudad = destino
        jugador.balance -= costo_total
        print(f"\nTe has movido a {destino}. Tu saldo actual es {jugador.balance} sheintavos.")
        input("\nPresiona Enter para continuar...")
    else:
        print("\nNo tienes suficientes sheintavos para moverte.")
        input("\nPresiona Enter para continuar...")

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
    
    # Ajuste de precios basado en la ciudad actual del jugador
    for recurso in RECURSOS:
        precio_ciudad = mercado.precios_por_ciudad[ciudad][recurso]
        print(f"- {recurso}: {precio_ciudad} sheintavos")

    print("\n¿Qué acción deseas realizar?")
    print("1. Comprar recursos")
    print("2. Vender recursos")
    print("3. Regresar")
    
    opcion = input("Elige una opción: ")

    if opcion == "1":
        recurso = input("¿Qué recurso quieres comprar? ")
        if recurso not in RECURSOS:
            print("Recurso no válido.")
            input("\nPresiona Enter para continuar...")
            return jugador
        cantidad = int(input(f"¿Cuántas unidades de {recurso} quieres comprar? "))
        precio_ciudad = mercado.precios_por_ciudad[ciudad][recurso]
        costo_total = precio_ciudad * cantidad
        if jugador.balance >= costo_total:
            jugador.balance -= costo_total
            jugador.inventario[recurso] += cantidad
            print(f"Has comprado {cantidad} unidades de {recurso}.")
            mercado.actualizar_precios(ciudad, recurso, cantidad)
            input("\nPresiona Enter para continuar...")
        else:
            print("No tienes suficientes sheintavos.")
            input("\nPresiona Enter para continuar...")

    elif opcion == "2":
        recurso = input("¿Qué recurso quieres vender? ")
        inventario = jugador.inventario
        if recurso not in inventario or inventario[recurso] <= 0:
            print("No tienes suficientes recursos para vender.")
            input("\nPresiona Enter para continuar...")
            return jugador
        cantidad = int(input(f"¿Cuántas unidades de {recurso} quieres vender? "))
        if cantidad > inventario[recurso]:
            print("No tienes tantas unidades para vender.")
            input("\nPresiona Enter para continuar...")
            return jugador
        precio_ciudad = mercado.precios_por_ciudad[ciudad][recurso]
        jugador.balance += precio_ciudad * cantidad
        jugador.inventario[recurso] -= cantidad
        if jugador.inventario[recurso] == 0:
            del jugador.inventario[recurso]
        print(f"Has vendido {cantidad} unidades de {recurso}.")
        mercado.actualizar_precios(ciudad, recurso, -cantidad)
        input("\nPresiona Enter para continuar...")
        
    return jugador

def mostrar_inventario(jugador, mercado):
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
    
    print("\n¿Qué acción deseas realizar?")
    print("1. Ver mejor estrategia para vender las cosas en el inventario")
    print("2. Regresar")
    
    opcion = input("Elige una opción: ")
    
    if opcion == "1":
        opciones_venta = calcular_mejor_venta(inventario, mercado.precios_por_ciudad, jugador.ciudad)
        
        print("\nMejores opciones de venta:")
        for opcion in opciones_venta:
            print(f"Ciudad: {opcion['ciudad']}, Recurso: {opcion['recurso']}, Cantidad: {opcion['cantidad']}, Ganancia: {opcion['ganancia']} sheintavos")
        
        input("\nPresiona Enter para continuar...")

def simular():
    jugadores_csv = leer_csv("datos/jugadores.csv")
    jugadores = cargar_jugadores_csv(jugadores_csv)
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
                
                if jugador_actual:
                    jugador_data = {
                        "nombre": jugador_actual.nombre,
                        "ciudad": jugador_actual.ciudad,
                        "balance": jugador_actual.balance
                    }
                    
                    jugadores_csv.append(jugador_data)
                    escribir_csv("datos/jugadores.csv", ["nombre", "ciudad", "balance"], jugadores_csv)
                    
                    jugadores_csv = leer_csv("datos/jugadores.csv")
                    jugadores = cargar_jugadores_csv(jugadores_csv)

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
                mostrar_inventario(jugador_actual, mercado)
            elif accion == "4":
                jugador_actual = None

if __name__ == "__main__":
    simular()