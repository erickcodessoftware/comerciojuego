from collections import defaultdict

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.inventario = defaultdict(int)
        self.balance = 100  # Saldo inicial del jugador

    def comerciar(self, recursos_pesos, precios, max_valor):
        """
        Optimiza la compra de recursos para maximizar el valor.

        Args:
            recursos_pesos (dict): Diccionario con los pesos de cada recurso. Ej: {"pan": 1, "agua": 2}.
            precios (dict): Diccionario con los precios de cada recurso. Ej: {"pan": 5, "agua": 3}.
            max_valor (int): Valor objetivo a maximizar basado en el inventario.

        Returns:
            bool: True si la optimización fue exitosa, False en caso contrario.
        """
        recursos = list(recursos_pesos.keys())
        n = len(recursos)
        balance_actual = self.balance

        # Crear la tabla DP para almacenar el valor máximo alcanzable
        dp = [[0 for _ in range(balance_actual + 1)] for _ in range(n + 1)]

        # Llenar la tabla usando programación dinámica
        for i in range(1, n + 1):
            recurso = recursos[i - 1]
            peso = recursos_pesos[recurso]
            precio = precios[recurso]
            for b in range(1, balance_actual + 1):
                if precio <= b:
                    dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - precio] + peso)
                else:
                    dp[i][b] = dp[i - 1][b]

        # Encontrar qué recursos se seleccionaron
        b = balance_actual
        for i in range(n, 0, -1):
            if dp[i][b] != dp[i - 1][b]:
                recurso = recursos[i - 1]
                self.inventario[recurso] += 1
                self.balance -= precios[recurso]
                b -= precios[recurso]

        return True

    def mostrar_inventario(self):
        """
        Muestra el inventario del jugador y su balance actual.
        """
        print(f"\n=== Inventario de {self.nombre} ===")
        for recurso, cantidad in self.inventario.items():
            print(f"- {recurso}: {cantidad} unidades")
        print(f"Saldo restante: {self.balance} sheintavos")
