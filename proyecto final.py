"""
PyRPG - Sistema de Gestión de Aventuras RPG (conserva en JSON)
Cubre:
- Registro / carga de jugadores (archivo players.json)
- Aventura conversacional con >=3 decisiones críticas por sesión
- Combates simples (daño, vida, resultado)
- Inventario (diccionarios), uso y descarte de ítems
- Guardado de progreso al finalizar la sesión
- Uso opcional de colorama (si está instalado) para mejorar salida
- Ejemplos de *args, lambdas y funciones anidadas
Ejecutar: python pyrpg.py
"""

import json
import os
import random
import sys

# Intentar usar colorama si está disponible (opcional)
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    def c(text, color=Fore.WHITE): return f"{color}{text}{Style.RESET_ALL}"
except Exception:
    # Fallback si no está instalado: función que devuelve texto sin color
    def c(text, color=None): return text

PLAYERS_FILE = "players.json"

# -------------------------
# Utilidades de almacenamiento
# -------------------------
def load_all_players():
    if not os.path.exists(PLAYERS_FILE):
        return {}
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_all_players(players):
    with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)

def save_player(player):
    players = load_all_players()
    players[player["nombre"]] = player
    save_all_players(players)

# -------------------------
# Helpers de juego
# -------------------------
def crear_inventario_default():
    # inventario como diccionario: item -> cantidad
    return {"pocion": 2, "antorcha": 1, "espada_baja": 1}

def elegir_clase_input():
    clases = {"1": "Guerrero", "2": "Mago", "3": "Explorador"}
    while True:
        print("Elige clase: 1) Guerrero 2) Mago 3) Explorador")
        k = input("> ").strip()
        if k in clases:
            return clases[k]
        print("Opción no válida, intenta de nuevo.")

def crear_jugador():
    nombre = input("Nombre del jugador: ").strip()
    if not nombre:
        print("Nombre no puede estar vacío.")
        return None
    clase = elegir_clase_input()
    player = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "xp": 0,
        "hp_max": 30 if clase == "Guerrero" else 20 if clase == "Mago" else 25,
        "hp": None,  # se inicializa abajo
        "ataque": 8 if clase == "Guerrero" else 10 if clase == "Mago" else 7,
        "defensa": 4 if clase == "Guerrero" else 2 if clase == "Mago" else 3,
        "inventario": crear_inventario_default(),
        "decisiones": []
    }
    player["hp"] = player["hp_max"]
    print(c(f"¡Bienvenido, {player['nombre']} el {player['clase']}!", None))
    save_player(player)
    return player

def cargar_jugador():
    players = load_all_players()
    if not players:
        print("No hay jugadores guardados.")
        return None
    print("Jugadores disponibles:")
    for i, name in enumerate(players.keys(), 1):
        print(f"{i}) {name}")
    choice = input("Escribe el nombre del jugador a cargar (exacto): ").strip()
    if choice in players:
        player = players[choice]
        print(c(f"Cargado: {player['nombre']} (Nivel {player['nivel']})", None))
        return player
    else:
        print("Nombre no encontrado.")
        return None

# -------------------------
# Funciones que usan *args, lambdas y anidadas
# -------------------------
def añadir_items(player, *items):
    """Ejemplo de uso de *args: añadir múltiples ítems al inventario."""
    inv = player["inventario"]
    for it in items:
        inv[it] = inv.get(it, 0) + 1
    print("Ítems añadidos:", ", ".join(items))
    save_player(player)

xp_para_nivel = lambda lvl: 100 * lvl  # lambda: XP necesaria para subir del nivel actual

def ganar_xp(player, cantidad):
    """Gana XP y sube de nivel si corresponde."""
    player["xp"] += cantidad
    while player["xp"] >= xp_para_nivel(player["nivel"]):
        player["xp"] -= xp_para_nivel(player["nivel"])
        player["nivel"] += 1
        # mejorar stats al subir
        player["hp_max"] += 5
        player["ataque"] += 1
        player["defensa"] += 1
        player["hp"] = player["hp_max"]
        print(c(f"¡Subiste al nivel {player['nivel']}! HP max ahora {player['hp_max']}", None))

# -------------------------
# Sistema de inventario (usar / descartar)
# -------------------------
def mostrar_inventario(player):
    print("Inventario:")
    for item, qty in player["inventario"].items():
        print(f"- {item}: {qty}")

def usar_item(player):
    mostrar_inventario(player)
    it = input("¿Qué ítem quieres usar? (escribe el nombre o 'cancel' para salir): ").strip().lower()
    if it == "cancel" or it == "":
        return
    inv = player["inventario"]
    if inv.get(it, 0) <= 0:
        print("No tienes ese ítem.")
        return
    # efectos básicos
    if it == "pocion":
        heal = 15
        player["hp"] = min(player["hp_max"], player["hp"] + heal)
        print(f"Usaste poción. Recuperaste {heal} HP. HP actual: {player['hp']}/{player['hp_max']}")
    elif it == "antorcha":
        print("Encendiste la antorcha. Ahora puedes ver mejor el camino.")
    elif it.startswith("espada"):
        print("Equipaste tu espada (brillante). Aumenta ataque temporalmente.")
        player["ataque"] += 2
    else:
        print("Usaste", it)
    inv[it] -= 1
    if inv[it] <= 0:
        del inv[it]
    save_player(player)

def descartar_item(player):
    mostrar_inventario(player)
    it = input("¿Qué ítem quieres descartar? (nombre o 'cancel'): ").strip().lower()
    if it == "cancel" or it == "":
        return
    inv = player["inventario"]
    if inv.get(it, 0) <= 0:
        print("No tienes ese ítem.")
        return
    cantidad = input("¿Cuántos deseas descartar? (enter para 1): ").strip()
    try:
        cantidad = int(cantidad) if cantidad else 1
    except:
        cantidad = 1
    inv[it] -= cantidad
    if inv[it] <= 0:
        inv.pop(it, None)
    print(f"Descartaste {cantidad}x {it}.")
    save_player(player)

# -------------------------
# Combate simple
# -------------------------
def combate(player, enemigo):
    """
    Simula un combate. enemigo es dict con 'nombre','hp','ataque','defensa','xp'
    Ejemplo de función anidada y lambda usage.
    """
    print(c(f"\n¡Combate: {enemigo['nombre']} te ataca!", None))
    # lambda para calcular daño base
    calc_dmg = lambda atk, defn: max(1, atk - defn + random.randint(-2, 2))

    # función anidada para ataque del enemigo
    def ataque_enemigo():
        dmg = calc_dmg(enemigo["ataque"], player["defensa"])
        player["hp"] -= dmg
        print(f"El {enemigo['nombre']} ataca y causa {dmg} de daño. Tu HP: {player['hp']}/{player['hp_max']}")

    # bucle de combate
    while enemigo["hp"] > 0 and player["hp"] > 0:
        print(f"\nTu vida: {player['hp']} | Vida del {enemigo['nombre']}: {enemigo['hp']}")
        print("Opciones: 1) Atacar 2) Defender (reduce daño) 3) Usar ítem 4) Huir")
        opt = input("> ").strip()
        if opt == "1" or opt.lower() == "atacar":
            dmg = calc_dmg(player["ataque"], enemigo.get("defensa", 0))
            enemigo["hp"] -= dmg
            print(f"Atacas y causas {dmg} de daño al {enemigo['nombre']}.")
            if enemigo["hp"] > 0:
                ataque_enemigo()
        elif opt == "2" or opt.lower() == "defender":
            # defender disminuye el daño entrante
            print("Te preparas para defender. Reduces el daño del próximo ataque.")
            orig_def = player["defensa"]
            player["defensa"] += 3
            ataque_enemigo()
            player["defensa"] = orig_def
        elif opt == "3" or opt.lower() == "usar":
            usar_item(player)
            # enemigo ataca después de que usas ítem (realismo)
            if enemigo["hp"] > 0:
                ataque_enemigo()
        elif opt == "4" or opt.lower() == "huir":
            chance = random.random()
            if chance < 0.5:
                print("Huyes con éxito del combate.")
                return False
            else:
                print("No logras huir. El enemigo aprovecha y ataca.")
                ataque_enemigo()
        else:
            print("Opción inválida.")
    # resultado
    if player["hp"] <= 0:
        print(c("Has sido derrotado...", None))
        return False
    else:
        print(c(f"Derrotaste al {enemigo['nombre']}!", None))
        ganar_xp(player, enemigo.get("xp", 20))
        # drop de ítem simple
        drop = enemigo.get("drop")
        if drop:
            añadir_items(player, drop)
        return True

# -------------------------
# Aventura conversacional (mínimo 3 decisiones)
# -------------------------
def aventura_session(player):
    print("\nTu aventura comienza en una aldea misteriosa...")
    decisiones_locales = []  # decisiones de esta sesión

    # Decision crítica 1
    print("\nTe acercas a una bifurcación en el bosque.")
    print("A) Ir por el camino oscuro\nB) Tomar el sendero iluminado")
    d1 = input("> ").strip().upper()
    if d1 == "A":
        print("El camino oscuro te lleva por ruinas antiguas. Encuentras una moneda vieja.")
        player["inventario"]["moneda_antigua"] = player["inventario"].get("moneda_antigua", 0) + 1
        decisiones_locales.append("Tomó camino oscuro")
    else:
        print("El sendero iluminado te hace sentir seguro. Un viajero te da una poción.")
        player["inventario"]["pocion"] = player["inventario"].get("pocion", 0) + 1
        decisiones_locales.append("Tomó sendero iluminado")

    # Decision crítica 2
    print("\nLlegas a una aldea: hay una taberna y un mercado.")
    print("1) Ir a la taberna (buscar rumores)\n2) Ir al mercado (comprar equipo)")
    d2 = input("> ").strip()
    if d2 == "1":
        print("En la taberna escuchas rumores de un goblin cerca del molino.")
        decisiones_locales.append("Taberna")
    else:
        print("En el mercado compras una antorcha a bajo costo.")
        player["inventario"]["antorcha"] = player["inventario"].get("antorcha", 0) + 1
        decisiones_locales.append("Mercado")

    # Encuentro con goblin (Decision crítica 3: pelear o evitar)
    print("\nMientras caminas, un goblin te ataca frente al molino.")
    print("Opciones: 1) Luchar 2) Huir 3) Intentar razonar")
    d3 = input("> ").strip()
    if d3 == "1":
        decisiones_locales.append("Luchó con goblin")
        goblin = {"nombre": "Goblin", "hp": 12, "ataque": 5, "defensa": 1, "xp": 40, "drop": "moneda_antigua"}
        combate(player, goblin)
    elif d3 == "2":
        print("Intentas huir. Corres y escapas, pero pierdes una poción por el camino.")
        if player["inventario"].get("pocion", 0) > 0:
            player["inventario"]["pocion"] -= 1
            if player["inventario"]["pocion"] <= 0:
                player["inventario"].pop("pocion", None)
        decisiones_locales.append("Huyó del goblin")
    else:
        # razonar - mini desafío
        print("Intentas razonar con el goblin (tirada de carisma simulada).")
        roll = random.randint(1, 20) + (player["nivel"] // 2)
        if roll >= 12:
            print("Convences al goblin. Te deja en paz y te regala una daga pequeña.")
            player["inventario"]["daga_pequeña"] = player["inventario"].get("daga_pequeña", 0) + 1
            decisiones_locales.append("Razonó con goblin y ganó")
        else:
            print("El goblin no te escucha y te ataca.")
            decisiones_locales.append("Razonó con goblin y falló")
            goblin = {"nombre": "Goblin", "hp": 12, "ataque": 5, "defensa": 1, "xp": 40}
            combate(player, goblin)

    # Opcional: más eventos/decisiones para ampliar la sesión
    # Pequeña misión: decidir ayudar a un aldeano
    print("\nUn aldeano te pide ayuda para encontrar a su gato perdido. ¿Ayudas? (s/n)")
    ans = input("> ").strip().lower()
    if ans == "s":
        print("Encuentras al gato y el aldeano te da experiencia por tu bondad.")
        ganar_xp(player, 20)
        decisiones_locales.append("Ayudó al aldeano")
    else:
        print("Decides no involucrarte.")
        decisiones_locales.append("No ayudó al aldeano")

    # Registrar decisiones de la sesión en el jugador
    player["decisiones"].extend(decisiones_locales)
    # Reparar HP si quedaron muy bajos pero no muertos
    if player["hp"] < 1:
        # jugador murió en batalla: restablecer a mitad de hp y perder algo (penalización leve)
        print("Has muerto durante la aventura. Se restaurará tu personaje parcialmente al terminar.")
        player["hp"] = max(1, player["hp_max"] // 2)
        # eliminar un item como penalización si existe
        if player["inventario"]:
            key = next(iter(player["inventario"].keys()))
            player["inventario"][key] -= 1
            if player["inventario"][key] <= 0:
                player["inventario"].pop(key, None)
            print(f"Perdiste 1x {key} como penalización.")
    print("\nFin de la sesión de aventura.")

# -------------------------
# Menú principal y flujo
# -------------------------
def main_menu():
    print(c("=== Bienvenido al mundo de PyRPG ===", None))
    while True:
        print("\n1) Registrar nuevo jugador\n2) Cargar jugador existente\n3) Salir")
        opt = input("> ").strip()
        if opt == "1":
            p = crear_jugador()
            if p:
                game_loop(p)
        elif opt == "2":
            p = cargar_jugador()
            if p:
                game_loop(p)
        elif opt == "3" or opt.lower() == "salir":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")

def game_loop(player):
    # loop para cada sesión con ese jugador
    while True:
        print(f"\n{player['nombre']} - Clase: {player['clase']} | Nivel: {player['nivel']} | HP: {player['hp']}/{player['hp_max']} | XP: {player['xp']}/{xp_para_nivel(player['nivel'])}")
        print("Menú: 1) Jugar sesión  2) Inventario  3) Guardar y salir  4) Eliminar jugador  5) Volver al menú principal")
        opt = input("> ").strip()
        if opt == "1":
            aventura_session(player)
        elif opt == "2":
            print("\nInventario y acciones:")
            print("a) Mostrar inventario  b) Usar ítem  c) Descartar ítem  d) Añadir ítem (debug)  e) Volver")
            o2 = input("> ").strip().lower()
            if o2 == "a":
                mostrar_inventario(player)
            elif o2 == "b":
                usar_item(player)
            elif o2 == "c":
                descartar_item(player)
            elif o2 == "d":
                # útil para pruebas: añadir items pasando *args
                añadir_items(player, "pocion", "moneda_antigua")
            else:
                pass
        elif opt == "3":
            print("Guardando progreso...")
            save_player(player)
            print("Progreso guardado. Volviendo al menú principal.")
            break
        elif opt == "4":
            conf = input("¿Estás seguro de eliminar este jugador? (s/n): ").strip().lower()
            if conf == "s":
                players = load_all_players()
                players.pop(player["nombre"], None)
                save_all_players(players)
                print("Jugador eliminado.")
                break
        elif opt == "5":
            print("Volviendo al menú principal.")
            break
        else:
            print("Opción inválida.")

# -------------------------
# Punto de entrada
# -------------------------
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nSalida interrumpida por usuario. Guardando si es necesario...")
        # no tenemos acceso al jugador actual desde aquí, así que solo cerramos
        sys.exit(0)
