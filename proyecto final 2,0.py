"""
PyRPG - Sistema de Gestión de Aventuras RPG (conserva en JSON)
Mejoras:
- Menús y elecciones totalmente numéricas (consistencia).
- Si el usuario ingresa una opción inválida: vuelve al menú padre.
- Mismos comportamientos y mecánicas del juego.
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
# Helpers de entrada/validación
# -------------------------
def ask_number(prompt, valid_set=None):
    """
    Pide un número al usuario. Si valid_set está dado (iterable), solo acepta valores en ese conjunto.
    Si la entrada no es válida, devuelve None (para indicar volver al menú).
    """
    s = input(prompt).strip()
    if not s.isdigit():
        print("Entrada inválida. Volviendo al menú anterior.")
        return None
    v = int(s)
    if valid_set is not None and v not in valid_set:
        print("Opción fuera de rango. Volviendo al menú anterior.")
        return None
    return v

# -------------------------
# Helpers de juego
# -------------------------
def crear_inventario_default():
    return {"pocion": 2, "antorcha": 1, "espada_baja": 1}

def elegir_clase_input():
    clases = {1: "Guerrero", 2: "Mago", 3: "Explorador"}
    print("Elige clase:")
    for k, v in clases.items():
        print(f"{k}) {v}")
    v = ask_number("> ", valid_set=set(clases.keys()))
    if v is None:
        return None
    return clases[v]

def crear_jugador():
    nombre = input("Nombre del jugador: ").strip()
    if not nombre:
        print("Nombre no puede estar vacío.")
        return None
    clase = elegir_clase_input()
    if clase is None:
        print("Creación cancelada (entrada inválida).")
        return None
    player = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "xp": 0,
        "hp_max": 30 if clase == "Guerrero" else 20 if clase == "Mago" else 25,
        "hp": None,
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
    names = list(players.keys())
    print("Jugadores disponibles:")
    for i, name in enumerate(names, 1):
        print(f"{i}) {name}")
    idx = ask_number("Elige el número del jugador a cargar: ", valid_set=set(range(1, len(names)+1)))
    if idx is None:
        return None
    chosen = names[idx-1]
    player = players[chosen]
    print(c(f"Cargado: {player['nombre']} (Nivel {player['nivel']})", None))
    return player

# -------------------------
# *args, lambdas y anidadas
# -------------------------
def añadir_items(player, *items):
    inv = player["inventario"]
    for it in items:
        inv[it] = inv.get(it, 0) + 1
    print("Ítems añadidos:", ", ".join(items))
    save_player(player)

xp_para_nivel = lambda lvl: 100 * lvl

def ganar_xp(player, cantidad):
    player["xp"] += cantidad
    while player["xp"] >= xp_para_nivel(player["nivel"]):
        player["xp"] -= xp_para_nivel(player["nivel"])
        player["nivel"] += 1
        player["hp_max"] += 5
        player["ataque"] += 1
        player["defensa"] += 1
        player["hp"] = player["hp_max"]
        print(c(f"¡Subiste al nivel {player['nivel']}! HP max ahora {player['hp_max']}", None))

# -------------------------
# Inventario
# -------------------------
def mostrar_inventario(player):
    print("Inventario:")
    for item, qty in player["inventario"].items():
        print(f"- {item}: {qty}")

def usar_item(player):
    mostrar_inventario(player)
    it = input("¿Qué ítem quieres usar? (escribe el nombre o enter para cancelar): ").strip().lower()
    if it == "":
        print("Acción cancelada. Volviendo al menú.")
        return
    inv = player["inventario"]
    if inv.get(it, 0) <= 0:
        print("No tienes ese ítem. Volviendo al menú.")
        return
    if it == "pocion":
        heal = 15
        player["hp"] = min(player["hp_max"], player["hp"] + heal)
        print(f"Usaste poción. Recuperaste {heal} HP. HP actual: {player['hp']}/{player['hp_max']}")
    elif it == "antorcha":
        print("Encendiste la antorcha. Ahora puedes ver mejor el camino.")
    elif it.startswith("espada"):
        print("Equipaste tu espada. Aumenta ataque temporalmente.")
        player["ataque"] += 2
    else:
        print("Usaste", it)
    inv[it] -= 1
    if inv[it] <= 0:
        del inv[it]
    save_player(player)

def descartar_item(player):
    mostrar_inventario(player)
    it = input("¿Qué ítem quieres descartar? (escribe el nombre o enter para cancelar): ").strip().lower()
    if it == "":
        print("Acción cancelada. Volviendo al menú.")
        return
    inv = player["inventario"]
    if inv.get(it, 0) <= 0:
        print("No tienes ese ítem. Volviendo al menú.")
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
    print(c(f"\n¡Combate: {enemigo['nombre']} te ataca!", None))
    calc_dmg = lambda atk, defn: max(1, atk - defn + random.randint(-2, 2))

    def ataque_enemigo():
        dmg = calc_dmg(enemigo["ataque"], player["defensa"])
        player["hp"] -= dmg
        print(f"El {enemigo['nombre']} ataca y causa {dmg} de daño. Tu HP: {player['hp']}/{player['hp_max']}")

    while enemigo["hp"] > 0 and player["hp"] > 0:
        print(f"\nTu vida: {player['hp']} | Vida del {enemigo['nombre']}: {enemigo['hp']}")
        print("Opciones: 1) Atacar  2) Defender  3) Usar ítem  4) Huir")
        opt = ask_number("> ", valid_set={1,2,3,4})
        if opt is None:
            print("Entrada inválida. Abortando combate y volviendo al menú.")
            return False
        if opt == 1:
            dmg = calc_dmg(player["ataque"], enemigo.get("defensa", 0))
            enemigo["hp"] -= dmg
            print(f"Atacas y causas {dmg} de daño al {enemigo['nombre']}.")
            if enemigo["hp"] > 0:
                ataque_enemigo()
        elif opt == 2:
            print("Te preparas para defender. Reduces el daño del próximo ataque.")
            orig_def = player["defensa"]
            player["defensa"] += 3
            ataque_enemigo()
            player["defensa"] = orig_def
        elif opt == 3:
            usar_item(player)
            if enemigo["hp"] > 0:
                ataque_enemigo()
        elif opt == 4:
            chance = random.random()
            if chance < 0.5:
                print("Huyes con éxito del combate.")
                return False
            else:
                print("No logras huir. El enemigo aprovecha y ataca.")
                ataque_enemigo()
    if player["hp"] <= 0:
        print(c("Has sido derrotado...", None))
        return False
    else:
        print(c(f"Derrotaste al {enemigo['nombre']}!", None))
        ganar_xp(player, enemigo.get("xp", 20))
        drop = enemigo.get("drop")
        if drop:
            añadir_items(player, drop)
        return True

# -------------------------
# Aventura conversacional (decisiones numéricas)
# -------------------------
def aventura_session(player):
    print("\nTu aventura comienza en una aldea misteriosa...")
    decisiones_locales = []

    # Decisión 1 (1/2)
    print("\nTe acercas a una bifurcación en el bosque.")
    print("1) Ir por el camino oscuro\n2) Tomar el sendero iluminado")
    d1 = ask_number("> ", valid_set={1,2})
    if d1 is None:
        print("Entrada inválida. Volviendo al menú de juego.")
        return
    if d1 == 1:
        print("El camino oscuro te lleva por ruinas antiguas. Encuentras una moneda vieja.")
        player["inventario"]["moneda_antigua"] = player["inventario"].get("moneda_antigua", 0) + 1
        decisiones_locales.append("Tomó camino oscuro")
    else:
        print("El sendero iluminado te hace sentir seguro. Un viajero te da una poción.")
        player["inventario"]["pocion"] = player["inventario"].get("pocion", 0) + 1
        decisiones_locales.append("Tomó sendero iluminado")

    # Decisión 2 (1/2)
    print("\nLlegas a una aldea: hay una taberna y un mercado.")
    print("1) Ir a la taberna (buscar rumores)\n2) Ir al mercado (comprar equipo)")
    d2 = ask_number("> ", valid_set={1,2})
    if d2 is None:
        print("Entrada inválida. Volviendo al menú de juego.")
        return
    if d2 == 1:
        print("En la taberna escuchas rumores de un goblin cerca del molino.")
        decisiones_locales.append("Taberna")
    else:
        print("En el mercado compras una antorcha a bajo costo.")
        player["inventario"]["antorcha"] = player["inventario"].get("antorcha", 0) + 1
        decisiones_locales.append("Mercado")

    # Decisión 3 (1/3)
    print("\nMientras caminas, un goblin te ataca frente al molino.")
    print("1) Luchar  2) Huir  3) Intentar razonar")
    d3 = ask_number("> ", valid_set={1,2,3})
    if d3 is None:
        print("Entrada inválida. Volviendo al menú de juego.")
        return
    if d3 == 1:
        decisiones_locales.append("Luchó con goblin")
        goblin = {"nombre": "Goblin", "hp": 12, "ataque": 5, "defensa": 1, "xp": 40, "drop": "moneda_antigua"}
        combate(player, goblin)
    elif d3 == 2:
        print("Intentas huir. Corres y escapas, pero pierdes una poción por el camino.")
        if player["inventario"].get("pocion", 0) > 0:
            player["inventario"]["pocion"] -= 1
            if player["inventario"]["pocion"] <= 0:
                player["inventario"].pop("pocion", None)
        decisiones_locales.append("Huyó del goblin")
    else:
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

    # Decisión extra (1/2)
    print("\nUn aldeano te pide ayuda para encontrar a su gato perdido.")
    print("1) Ayudar  2) No ayudar")
    ans = ask_number("> ", valid_set={1,2})
    if ans is None:
        print("Entrada inválida. Volviendo al menú de juego.")
        return
    if ans == 1:
        print("Encuentras al gato y el aldeano te da experiencia por tu bondad.")
        ganar_xp(player, 20)
        decisiones_locales.append("Ayudó al aldeano")
    else:
        print("Decides no involucrarte.")
        decisiones_locales.append("No ayudó al aldeano")

    player["decisiones"].extend(decisiones_locales)
    if player["hp"] < 1:
        print("Has muerto durante la aventura. Se restaurará tu personaje parcialmente al terminar.")
        player["hp"] = max(1, player["hp_max"] // 2)
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
        opt = ask_number("> ", valid_set={1,2,3})
        if opt is None:
            continue  # inválido: volver a mostrar menú principal
        if opt == 1:
            p = crear_jugador()
            if p:
                game_loop(p)
        elif opt == 2:
            p = cargar_jugador()
            if p:
                game_loop(p)
        elif opt == 3:
            print("Hasta luego.")
            break

def game_loop(player):
    while True:
        print(f"\n{player['nombre']} - Clase: {player['clase']} | Nivel: {player['nivel']} | HP: {player['hp']}/{player['hp_max']} | XP: {player['xp']}/{xp_para_nivel(player['nivel'])}")
        print("Menú:")
        print("1) Jugar sesión")
        print("2) Inventario")
        print("3) Guardar y salir")
        print("4) Eliminar jugador")
        print("5) Volver al menú principal")
        opt = ask_number("> ", valid_set={1,2,3,4,5})
        if opt is None:
            # Entrada inválida: regresar al menú principal (según petición)
            print("Entrada inválida. Volviendo al menú principal.")
            return
        if opt == 1:
            aventura_session(player)
        elif opt == 2:
            # Submenú inventario (numérico)
            print("\nInventario y acciones:")
            print("1) Mostrar inventario")
            print("2) Usar ítem")
            print("3) Descartar ítem")
            print("4) Añadir ítem (debug)")
            print("5) Volver")
            o2 = ask_number("> ", valid_set={1,2,3,4,5})
            if o2 is None or o2 == 5:
                continue  # volver al game menu
            if o2 == 1:
                mostrar_inventario(player)
            elif o2 == 2:
                usar_item(player)
            elif o2 == 3:
                descartar_item(player)
            elif o2 == 4:
                añadir_items(player, "pocion", "moneda_antigua")
        elif opt == 3:
            print("Guardando progreso...")
            save_player(player)
            print("Progreso guardado. Volviendo al menú principal.")
            return
        elif opt == 4:
            print("¿Estás seguro de eliminar este jugador?")
            print("1) Sí\n2) No")
            conf = ask_number("> ", valid_set={1,2})
            if conf is None or conf == 2:
                print("Cancelado. Volviendo al menú principal del jugador.")
                continue
            players = load_all_players()
            players.pop(player["nombre"], None)
            save_all_players(players)
            print("Jugador eliminado.")
            return
        elif opt == 5:
            print("Volviendo al menú principal.")
            return

# -------------------------
# Punto de entrada
# -------------------------
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nSalida interrumpida por usuario. Saliendo...")
        sys.exit(0)
