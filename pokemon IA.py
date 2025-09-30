import random
import time
import os
import json

# -----------------------------
# Dibujos ASCII sencillos
# -----------------------------
ascii_art = {
    "Flameragon": r"""
      /^\/^\
    _|__|  O|
\\/     /~     \\
 \____|________/
       \_______/
    """,
    "Aquatle": r"""
     ><(((('> 
    """,
    "Leafox": r"""
    (\__/)
    ( •.•)
    c(")(")
    """,
    "Normie": r"""
    (•_•) 
    <)   )╯
    /   \\
    """,
    "Sparkit": r"""
     =^.^=
    """,
    "Wavefin": r"""
     ><>
    """,
    "Bushbug": r"""
     _/\_
    (o  o)
    / -- \\
    """,
    "Fluffball": r"""
     (o.o)
    <)   (>
     ^^ ^^
    """,
    "Rocktoise": r"""
     ____
   /      \\
  |  () () |
   \  __  /
    """,
    "Glowfly": r"""
     \*o*/ 
      / \\
    """
}

# -----------------------------
# Tabla de efectividades
# (lista, no diccionario)
# -----------------------------
type_effectiveness_table = [
    ['fuego', 'planta', 2.0],
    ['fuego', 'agua', 0.5],
    ['fuego', 'normal', 1.0],
    ['agua', 'fuego', 2.0],
    ['agua', 'planta', 0.5],
    ['agua', 'normal', 1.0],
    ['planta', 'agua', 2.0],
    ['planta', 'fuego', 0.5],
    ['planta', 'normal', 1.0],
    ['normal', 'fuego', 1.0],
    ['normal', 'agua', 1.0],
    ['normal', 'planta', 1.0]
]

# -----------------------------
# Clase Movimiento
# -----------------------------
class Movimiento:
    def __init__(self, nombre, poder, tipo):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo

    def atacar(self):
        efecto = random.randint(1, 10)
        if efecto <= 2:
            return 0, "Sin efecto"
        elif efecto <= 7:
            return self.poder, "Ataque básico"
        elif efecto <= 9:
            return int(self.poder * 1.5), "Ataque doble"
        else:
            return 0, "Ataque pierde turno"


# -----------------------------
# Clase Pokemon
# -----------------------------
class Pokemon:
    def __init__(self, nombre, tipo, ataque, defensa, hp, habilidad, movimientos):
        self.nombre = nombre
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.hp_max = hp
        self.hp_actual = hp
        self.habilidad = habilidad
        self.movimientos = movimientos

    def mostrar_ascii(self):
        art = ascii_art.get(self.nombre)
        if art:
            print(art)

    def calcular_efectividad(self, tipo_oponente):
        for efectividad in type_effectiveness_table:
            if efectividad[0] == self.tipo and efectividad[1] == tipo_oponente:
                return efectividad[2]
        return 1.0

    def cuackatacar(self, movimiento_idx, oponente):
        movimiento = self.movimientos[movimiento_idx]
        danio_base, mensaje = movimiento.atacar()

        if danio_base == 0:
            return mensaje

        # STAB
        stab = 1.5 if movimiento.tipo == self.tipo else 1.0

        efectividad = self.calcular_efectividad(oponente.tipo)

        danio_final = int((danio_base * self.ataque / max(1, oponente.defensa)) * stab * efectividad)

        oponente.hp_actual = max(0, oponente.hp_actual - danio_final)

        mensaje_efectividad = ""
        if efectividad > 1:
            mensaje_efectividad = " ¡Es super efectivo!"
        elif efectividad < 1:
            mensaje_efectividad = " ¡No es muy efectivo..."

        return f"{mensaje}{mensaje_efectividad} ¡{danio_final} de daño!"

    def cuackhabilidad(self):
        return self.habilidad

    def cuackevolucionar(self):
        return None


# -----------------------------
# Clases específicas
# -----------------------------
class Flameragon(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Llamarada", 40, "fuego"),
            Movimiento("Ascuas", 30, "fuego"),
            Movimiento("Garra", 25, "normal"),
            Movimiento("Gruñido", 0, "normal")
        ]
        super().__init__("Flameragon", "fuego", 52, 43, 39, "Mar llamas", movimientos)


class Aquatle(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Pistola Agua", 40, "agua"),
            Movimiento("Burbujas", 30, "agua"),
            Movimiento("Cabezazo", 25, "normal"),
            Movimiento("Retirada", 0, "normal")
        ]
        super().__init__("Aquatle", "agua", 48, 65, 44, "Torrente", movimientos)


class Leafox(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Latigazo", 40, "planta"),
            Movimiento("Hoja Afilada", 30, "planta"),
            Movimiento("Derribo", 25, "normal"),
            Movimiento("Crecimiento", 0, "normal")
        ]
        super().__init__("Leafox", "planta", 49, 49, 45, "Espesura", movimientos)


class Normie(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Placaje", 35, "normal"),
            Movimiento("Ataque Rápido", 30, "normal"),
            Movimiento("Doble Filo", 40, "normal"),
            Movimiento("Canto", 0, "normal")
        ]
        super().__init__("Normie", "normal", 55, 50, 50, "Fuga", movimientos)


class Sparkit(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Chispa", 35, "fuego"),
            Movimiento("Arañazo", 25, "normal")
        ]
        super().__init__("Sparkit", "fuego", 45, 40, 35, "Electricidad", movimientos)


class Wavefin(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Surf", 35, "agua"),
            Movimiento("Mordisco", 25, "normal")
        ]
        super().__init__("Wavefin", "agua", 42, 50, 40, "Nado", movimientos)


class Bushbug(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Hoja Navaja", 35, "planta"),
            Movimiento("Picotazo", 25, "normal")
        ]
        super().__init__("Bushbug", "planta", 40, 45, 42, "Enjambre", movimientos)


class Fluffball(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Golpe Cuerpo", 35, "normal"),
            Movimiento("Lengüetazo", 25, "normal")
        ]
        super().__init__("Fluffball", "normal", 50, 45, 48, "Pelusa", movimientos)


class Rocktoise(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Roca Afilada", 35, "normal"),
            Movimiento("Defensa", 0, "normal")
        ]
        super().__init__("Rocktoise", "normal", 48, 65, 44, "Caparazón", movimientos)


class Glowfly(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Destello", 30, "normal"),
            Movimiento("Polvo Cegador", 0, "normal")
        ]
        super().__init__("Glowfly", "normal", 42, 38, 40, "Iluminación", movimientos)


# -----------------------------
# Jugador
# -----------------------------
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.equipo = []
        self.pokemon_actual = None
        self.historial_combates = []

    def agregar_pokemon(self, pokemon):
        if len(self.equipo) < 6:
            self.equipo.append(pokemon)
            if not self.pokemon_actual:
                self.pokemon_actual = pokemon
            return True
        return False

    def cambiar_pokemon_actual(self, idx):
        if 0 <= idx < len(self.equipo) and self.equipo[idx].hp_actual > 0:
            self.pokemon_actual = self.equipo[idx]
            return True
        return False


# -----------------------------
# Juego
# -----------------------------
class Juego:
    def __init__(self):
        self.jugador = None
        # Guardamos clases (no instancias) para crear nuevos salvajes cada vez
        self.pokemon_salvajes = [Sparkit, Wavefin, Bushbug, Fluffball,
                                 Rocktoise, Glowfly, Flameragon, Aquatle, Leafox, Normie]
        self.mapa = []
        self.tamano_mapa = 15
        self.posicion_jugador = [7, 7]
        self.pokemon_en_mapa = []
        self.inicializar_mapa()

    def inicializar_mapa(self):
        # Re-crear mapa y colocar pokémon frescos
        self.mapa = [['.' for _ in range(self.tamano_mapa)] for _ in range(self.tamano_mapa)]
        self.pokemon_en_mapa = []
        for _ in range(5):
            x = random.randint(0, self.tamano_mapa - 1)
            y = random.randint(0, self.tamano_mapa - 1)
            pokemon_cls = random.choice(self.pokemon_salvajes)
            pokemon = pokemon_cls()  # instancia nueva
            self.pokemon_en_mapa.append({'x': x, 'y': y, 'pokemon': pokemon, 'emoji': '🐾'})

    def mostrar_mapa(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔" + "═" * (self.tamano_mapa * 2 - 1) + "╗")

        for y in range(self.tamano_mapa):
            linea = "║"
            for x in range(self.tamano_mapa):
                if x == self.posicion_jugador[0] and y == self.posicion_jugador[1]:
                    linea += "😀"
                else:
                    emoji_encontrado = False
                    for pokemon in self.pokemon_en_mapa:
                        if pokemon['x'] == x and pokemon['y'] == y:
                            linea += pokemon['emoji']
                            emoji_encontrado = True
                            break
                    if not emoji_encontrado:
                        linea += "· "
            linea += "║"
            print(linea)

        print("╚" + "═" * (self.tamano_mapa * 2 - 1) + "╝")
        print("WASD - mover   E - Estado equipo   H - Historial   V - Volver   G - Guardar")

    def mover_jugador(self, direccion):
        x, y = self.posicion_jugador

        if direccion == 'w' and y > 0:
            y -= 1
        elif direccion == 's' and y < self.tamano_mapa - 1:
            y += 1
        elif direccion == 'a' and x > 0:
            x -= 1
        elif direccion == 'd' and x < self.tamano_mapa - 1:
            x += 1
        else:
            return False

        self.posicion_jugador = [x, y]

        # Mover Pokémon en el mapa aleatoriamente
        for pokemon in self.pokemon_en_mapa:
            mov_x = random.choice([-1, 0, 1])
            mov_y = random.choice([-1, 0, 1])
            nuevo_x = max(0, min(self.tamano_mapa - 1, pokemon['x'] + mov_x))
            nuevo_y = max(0, min(self.tamano_mapa - 1, pokemon['y'] + mov_y))
            pokemon['x'] = nuevo_x
            pokemon['y'] = nuevo_y

        # Verificar encuentro con Pokémon salvaje
        for pokemon_dict in list(self.pokemon_en_mapa):
            if pokemon_dict['x'] == x and pokemon_dict['y'] == y:
                # Lanzar combate con la instancia específica
                self.combate(pokemon_dict['pokemon'])
                # Después del combate, reiniciamos el mapa (según petición)
                self.inicializar_mapa()
                return True

        return True

    def combate(self, pokemon_salvaje):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"¡Un {pokemon_salvaje.nombre} salvaje apareció!")
        pokemon_salvaje.mostrar_ascii()
        time.sleep(1)

        # Bucle de combate
        while self.jugador.pokemon_actual and self.jugador.pokemon_actual.hp_actual > 0 and pokemon_salvaje.hp_actual > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Tu {self.jugador.pokemon_actual.nombre}: {self.jugador.pokemon_actual.hp_actual}/{self.jugador.pokemon_actual.hp_max} HP")
            self.jugador.pokemon_actual.mostrar_ascii()
            print(f"{pokemon_salvaje.nombre} salvaje: {pokemon_salvaje.hp_actual}/{pokemon_salvaje.hp_max} HP")
            pokemon_salvaje.mostrar_ascii()

            print("\n¿Qué deseas hacer?")
            print("1. Luchar")
            print("2. Estado")
            print("3. Huir")

            opcion = input("> ")

            if opcion == "1":
                print("\nElige un movimiento:")
                for i, movimiento in enumerate(self.jugador.pokemon_actual.movimientos):
                    print(f"{i+1}. {movimiento.nombre} ({movimiento.tipo})")

                try:
                    mov_opcion = int(input("> ")) - 1
                    if 0 <= mov_opcion < len(self.jugador.pokemon_actual.movimientos):
                        print(f"\n{self.jugador.pokemon_actual.nombre} usa {self.jugador.pokemon_actual.movimientos[mov_opcion].nombre}!")
                        resultado = self.jugador.pokemon_actual.cuackatacar(mov_opcion, pokemon_salvaje)
                        print(resultado)
                    else:
                        print("\nMovimiento no válido")
                        time.sleep(1)
                        continue
                except ValueError:
                    print("\nOpción no válida")
                    time.sleep(1)
                    continue

                if pokemon_salvaje.hp_actual <= 0:
                    print(f"\n¡{pokemon_salvaje.nombre} salvaje fue derrotado!")
                    self.jugador.historial_combates.append(f"Victoria contra {pokemon_salvaje.nombre}")
                    time.sleep(2)
                    break

                # Turno del Pokémon salvaje
                mov_salvaje = random.randint(0, len(pokemon_salvaje.movimientos) - 1)
                print(f"\n{pokemon_salvaje.nombre} salvaje usa {pokemon_salvaje.movimientos[mov_salvaje].nombre}!")
                resultado = pokemon_salvaje.cuackatacar(mov_salvaje, self.jugador.pokemon_actual)
                print(resultado)

                if self.jugador.pokemon_actual.hp_actual <= 0:
                    print(f"\n¡Tu {self.jugador.pokemon_actual.nombre} fue derrotado!")
                    self.jugador.historial_combates.append(f"Derrota contra {pokemon_salvaje.nombre}")

                    # Verificar si hay más Pokémon en el equipo
                    pokemon_vivos = [p for p in self.jugador.equipo if p.hp_actual > 0]
                    if pokemon_vivos:
                        print("\nElige otro Pokémon:")
                        for i, p in enumerate(self.jugador.equipo):
                            estado = "💀" if p.hp_actual <= 0 else "❤️"
                            print(f"{i+1}. {p.nombre} {estado} {p.hp_actual}/{p.hp_max} HP")

                        try:
                            pokemon_opcion = int(input("> ")) - 1
                            if 0 <= pokemon_opcion < len(self.jugador.equipo) and self.jugador.equipo[pokemon_opcion].hp_actual > 0:
                                self.jugador.pokemon_actual = self.jugador.equipo[pokemon_opcion]
                                print(f"\n¡Adelante {self.jugador.pokemon_actual.nombre}!")
                                time.sleep(1)
                            else:
                                # Si entrada inválida, seleccionar el primero vivo automáticamente
                                self.jugador.pokemon_actual = pokemon_vivos[0]
                                print(f"\nSe seleccionó automáticamente a {self.jugador.pokemon_actual.nombre}.")
                                time.sleep(1)
                        except ValueError:
                            self.jugador.pokemon_actual = pokemon_vivos[0]
                            print(f"\nSe seleccionó automáticamente a {self.jugador.pokemon_actual.nombre}.")
                            time.sleep(1)
                    else:
                        print("\n¡Todos tus Pokémon fueron derrotados!")
                        time.sleep(2)
                        break

                time.sleep(2)

            elif opcion == "2":
                self.mostrar_estado_combate()
                input("\nPresiona Enter para continuar...")

            elif opcion == "3":
                print("\nLograste huir del combate")
                self.jugador.historial_combates.append(f"Huiste de {pokemon_salvaje.nombre}")
                time.sleep(1)
                break

            else:
                print("\nOpción no válida")
                time.sleep(1)

    def mostrar_estado_equipo(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Estado del equipo de {self.jugador.nombre}:")
        print()
        for i, pokemon in enumerate(self.jugador.equipo):
            estado = "💀" if pokemon.hp_actual <= 0 else "❤️"
            print(f"{i+1}. {pokemon.nombre} ({pokemon.tipo}) {estado} {pokemon.hp_actual}/{pokemon.hp_max} HP")
            print(f"   Habilidad: {pokemon.cuackhabilidad()}")
            print(f"   Movimientos: {', '.join([m.nombre for m in pokemon.movimientos])}")
            pokemon.mostrar_ascii()
            print()
        input("\nPresiona Enter para continuar...")

    def mostrar_estado_combate(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if not self.jugador.pokemon_actual:
            print("No tienes un Pokémon activo.")
            return
        print(f"Estado de {self.jugador.pokemon_actual.nombre}:")
        self.jugador.pokemon_actual.mostrar_ascii()
        print(f"HP: {self.jugador.pokemon_actual.hp_actual}/{self.jugador.pokemon_actual.hp_max}")
        print(f"Tipo: {self.jugador.pokemon_actual.tipo}")
        print(f"Habilidad: {self.jugador.pokemon_actual.cuackhabilidad()}")
        print("Movimientos:")
        for movimiento in self.jugador.pokemon_actual.movimientos:
            print(f"  - {movimiento.nombre} ({movimiento.tipo}, Poder: {movimiento.poder})")

    def mostrar_historial(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Historial de combates:")
        if not self.jugador.historial_combates:
            print("No hay combates registrados")
        else:
            for i, combate in enumerate(self.jugador.historial_combates, 1):
                print(f"{i}. {combate}")
        input("\nPresiona Enter para continuar...")

    def guardar_partida(self):
        datos = {
            'nombre': self.jugador.nombre,
            'equipo': [],
            'pokemon_actual': 0,
            'historial_combates': self.jugador.historial_combates
        }

        for i, pokemon in enumerate(self.jugador.equipo):
            if pokemon == self.jugador.pokemon_actual:
                datos['pokemon_actual'] = i

            pokemon_data = {
                'nombre': pokemon.nombre,
                'tipo': pokemon.tipo,
                'ataque': pokemon.ataque,
                'defensa': pokemon.defensa,
                'hp_max': pokemon.hp_max,
                'hp_actual': pokemon.hp_actual,
                'habilidad': pokemon.habilidad,
                'movimientos': []
            }

            for movimiento in pokemon.movimientos:
                pokemon_data['movimientos'].append({
                    'nombre': movimiento.nombre,
                    'poder': movimiento.poder,
                    'tipo': movimiento.tipo
                })

            datos['equipo'].append(pokemon_data)

        with open('partida_guardada.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        print("Partida guardada correctamente")
        time.sleep(1)

    def cargar_partida(self):
        try:
            with open('partida_guardada.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)

            self.jugador = Jugador(datos['nombre'])
            self.jugador.historial_combates = datos.get('historial_combates', [])

            for pokemon_data in datos['equipo']:
                movimientos = []
                for mov_data in pokemon_data['movimientos']:
                    movimientos.append(Movimiento(mov_data['nombre'], mov_data['poder'], mov_data['tipo']))

                # Determinar la clase correcta del Pokémon
                nombre = pokemon_data['nombre']
                if nombre == "Flameragon":
                    pokemon = Flameragon()
                elif nombre == "Aquatle":
                    pokemon = Aquatle()
                elif nombre == "Leafox":
                    pokemon = Leafox()
                elif nombre == "Normie":
                    pokemon = Normie()
                elif nombre == "Sparkit":
                    pokemon = Sparkit()
                elif nombre == "Wavefin":
                    pokemon = Wavefin()
                elif nombre == "Bushbug":
                    pokemon = Bushbug()
                elif nombre == "Fluffball":
                    pokemon = Fluffball()
                elif nombre == "Rocktoise":
                    pokemon = Rocktoise()
                elif nombre == "Glowfly":
                    pokemon = Glowfly()
                else:
                    pokemon = Pokemon(pokemon_data['nombre'], pokemon_data['tipo'],
                                      pokemon_data['ataque'], pokemon_data['defensa'],
                                      pokemon_data['hp_max'], pokemon_data.get('habilidad', ''), movimientos)

                # Actualizar stats
                pokemon.ataque = pokemon_data['ataque']
                pokemon.defensa = pokemon_data['defensa']
                pokemon.hp_max = pokemon_data['hp_max']
                pokemon.hp_actual = pokemon_data['hp_actual']

                self.jugador.equipo.append(pokemon)

            # Establecer pokemon actual
            idx_actual = datos.get('pokemon_actual', 0)
            if 0 <= idx_actual < len(self.jugador.equipo):
                self.jugador.pokemon_actual = self.jugador.equipo[idx_actual]
            elif self.jugador.equipo:
                self.jugador.pokemon_actual = self.jugador.equipo[0]

            print("Partida cargada correctamente")
            time.sleep(1)
            return True

        except FileNotFoundError:
            print("No hay partida guardada")
            time.sleep(1)
            return False

    def crear_partida(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        nombre = input("Ingresa tu nombre: ")
        self.jugador = Jugador(nombre)

        print("\nElige tu Pokémon inicial:")
        print("1. Flameragon (Tipo fuego)")
        print("2. Aquatle (Tipo agua)")
        print("3. Leafox (Tipo planta)")

        while True:
            opcion = input("> ")
            if opcion == "1":
                self.jugador.agregar_pokemon(Flameragon())
                break
            elif opcion == "2":
                self.jugador.agregar_pokemon(Aquatle())
                break
            elif opcion == "3":
                self.jugador.agregar_pokemon(Leafox())
                break
            else:
                print("Opción no válida")

        print(f"\n¡Felicidades {nombre}! Has recibido un {self.jugador.pokemon_actual.nombre}")
        time.sleep(2)

    def menu_principal(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== MENÚ PRINCIPAL ===")
            print("1. Crear partida")
            print("2. Continuar partida")
            print("3. Borrar partida")
            print("4. Salir")

            opcion = input("> ")

            if opcion == "1":
                self.crear_partida()
                self.explorar()
            elif opcion == "2":
                if self.cargar_partida():
                    self.explorar()
            elif opcion == "3":
                try:
                    os.remove('partida_guardada.json')
                    print("Partida borrada")
                    time.sleep(1)
                except FileNotFoundError:
                    print("No hay partida guardada")
                    time.sleep(1)
            elif opcion == "4":
                print("¡Hasta pronto!")
                break
            else:
                print("Opción no válida")
                time.sleep(1)

    def explorar(self):
        while True:
            self.mostrar_mapa()
            comando = input("> ").lower()

            if comando in ['w', 'a', 's', 'd']:
                self.mover_jugador(comando)
            elif comando == 'e':
                self.mostrar_estado_equipo()
            elif comando == 'v':
                break
            elif comando == 'h':
                self.mostrar_historial()
            elif comando == 'g':
                if self.jugador:
                    self.guardar_partida()
            else:
                print("Comando no válido")
                time.sleep(1)


# -----------------------------
# Función principal
# -----------------------------

def main():
    juego = Juego()
    juego.menu_principal()


if __name__ == "__main__":
    main()
