#!/usr/bin/env python3
"""
Gestor de estudiantes mejorado
Funciones añadidas:
- Agregar nuevo estudiante
- Mostrar todos los estudiantes
- Calcular promedio por ID
- Eliminar estudiante
- Editar estudiante (nombre, edad, calificaciones: reemplazar/añadir/quitar)
- Añadir calificación rápida a un estudiante
- Búsqueda por nombre parcial (case-insensitive)
- Estadísticas del grupo: promedio general, nota máxima y mínima y estudiantes asociados, mejor promedio
- Guardar/Cargar desde archivo estudiantes.json
Menú numérico consistente y validaciones.
"""

import json
import os
import sys

FILENAME = "estudiantes.json"


# -------------------------
# Persistencia
# -------------------------
def cargar_desde_archivo():
    if not os.path.exists(FILENAME):
        return {}
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            # normalizar calificaciones a lista de floats
            for k, v in data.items():
                v["calificaciones"] = [float(x) for x in v.get("calificaciones", [])]
            return data
    except Exception as e:
        print("Error al cargar archivo:", e)
        return {}


def guardar_en_archivo(estudiantes):
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(estudiantes, f, indent=2, ensure_ascii=False)
        print(f"Guardado en '{FILENAME}'.")
    except Exception as e:
        print("Error al guardar archivo:", e)


# -------------------------
# Validaciones y utilidades
# -------------------------
def pedir_texto(prompt, obligatorio=True):
    s = input(prompt).strip()
    if obligatorio and s == "":
        print("Entrada requerida.")
        return None
    return s


def pedir_entero(prompt, minimo=None):
    s = input(prompt).strip()
    if s == "":
        print("Entrada requerida.")
        return None
    try:
        val = int(s)
    except ValueError:
        print("Debe ser un número entero.")
        return None
    if minimo is not None and val < minimo:
        print(f"El número debe ser >= {minimo}.")
        return None
    return val


def parsear_calificaciones(s):
    """
    Acepta entrada como '90 80 75' o '90,80,75' o '90;80;75'
    Devuelve lista de floats o None si hay error.
    """
    if s is None:
        return None
    s = s.strip()
    if s == "":
        return []
    for sep in (",", ";"):
        s = s.replace(sep, " ")
    partes = [p for p in s.split() if p != ""]
    califs = []
    try:
        for p in partes:
            val = float(p)
            if val < 0 or val > 100:
                print("Las calificaciones deben estar entre 0 y 100.")
                return None
            califs.append(val)
    except ValueError:
        print("Las calificaciones deben ser números.")
        return None
    return califs


def calcular_promedio(calificaciones):
    if not calificaciones:
        return None
    return sum(calificaciones) / len(calificaciones)


# -------------------------
# Operaciones principales
# -------------------------
def agregar_estudiante(estudiantes):
    print("\n--- Agregar nuevo estudiante ---")
    id_ = pedir_texto("ID (ej. A001): ")
    if id_ is None:
        return
    if id_ in estudiantes:
        print("Ya existe un estudiante con esa ID.")
        return
    nombre = pedir_texto("Nombre completo: ")
    if nombre is None:
        return
    edad = pedir_entero("Edad: ", minimo=0)
    if edad is None:
        return
    raw = pedir_texto("Calificaciones iniciales (espacio/coma/; separador) - dejar vacío si none: ", obligatorio=False)
    califs = parsear_calificaciones(raw or "")
    if califs is None:
        return
    estudiantes[id_] = {"nombre": nombre, "edad": edad, "calificaciones": califs}
    print(f"Estudiante {id_} agregado.")


def mostrar_todos(estudiantes):
    print("\n--- Lista de estudiantes ---")
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    for id_, info in estudiantes.items():
        prom = calcular_promedio(info["calificaciones"])
        prom_text = f"{prom:.2f}" if prom is not None else "N/A"
        print(f"Estudiante {id_} - {info['nombre']} - Edad: {info['edad']} - Promedio: {prom_text}")


def promedio_por_id(estudiantes):
    print("\n--- Calcular promedio por ID ---")
    id_ = pedir_texto("ID del estudiante: ")
    if id_ is None:
        return
    if id_ not in estudiantes:
        print("ID no encontrada.")
        return
    info = estudiantes[id_]
    prom = calcular_promedio(info["calificaciones"])
    if prom is None:
        print(f"{id_} - {info['nombre']} no tiene calificaciones.")
    else:
        print(f"{id_} - {info['nombre']} - Promedio: {prom:.2f}")


def eliminar_estudiante(estudiantes):
    print("\n--- Eliminar estudiante ---")
    id_ = pedir_texto("ID del estudiante a eliminar: ")
    if id_ is None:
        return
    if id_ not in estudiantes:
        print("ID no encontrada.")
        return
    confirm = pedir_texto(f"Confirma eliminar {id_} - {estudiantes[id_]['nombre']} (s/n): ")
    if confirm is None or confirm.lower() != "s":
        print("Eliminación cancelada.")
        return
    estudiantes.pop(id_)
    print("Estudiante eliminado.")


# -------------------------
# Funciones nuevas: edición y calificaciones
# -------------------------
def editar_estudiante(estudiantes):
    print("\n--- Editar estudiante ---")
    id_ = pedir_texto("ID del estudiante a editar: ")
    if id_ is None:
        return
    if id_ not in estudiantes:
        print("ID no encontrada.")
        return
    info = estudiantes[id_]
    while True:
        print(f"\nEditando {id_} - {info['nombre']}")
        print("1) Modificar nombre")
        print("2) Modificar edad")
        print("3) Reemplazar lista de calificaciones")
        print("4) Añadir calificaciones (varias)")
        print("5) Eliminar calificación por índice")
        print("6) Ver calificaciones actuales")
        print("7) Volver")
        opt = pedir_entero("> ")
        if opt is None:
            print("Entrada inválida. Volviendo al menú de edición.")
            return
        if opt == 1:
            nuevo = pedir_texto("Nuevo nombre completo: ")
            if nuevo:
                info["nombre"] = nuevo
                print("Nombre actualizado.")
        elif opt == 2:
            nueva_edad = pedir_entero("Nueva edad: ", minimo=0)
            if nueva_edad is not None:
                info["edad"] = nueva_edad
                print("Edad actualizada.")
        elif opt == 3:
            raw = pedir_texto("Introduce nuevas calificaciones (separadas por espacio/coma): ", obligatorio=False)
            califs = parsear_calificaciones(raw or "")
            if califs is None:
                print("No se actualizó la lista de calificaciones.")
            else:
                info["calificaciones"] = califs
                print("Calificaciones reemplazadas.")
        elif opt == 4:
            raw = pedir_texto("Añadir calificaciones (separadas por espacio/coma): ", obligatorio=False)
            califs = parsear_calificaciones(raw or "")
            if califs is None:
                print("No se añadieron calificaciones.")
            else:
                info["calificaciones"].extend(califs)
                print("Calificaciones añadidas.")
        elif opt == 5:
            if not info["calificaciones"]:
                print("No hay calificaciones para eliminar.")
            else:
                print("Calificaciones actuales:")
                for i, val in enumerate(info["calificaciones"], 1):
                    print(f"{i}) {val}")
                idx = pedir_entero("Índice de calificación a eliminar (número): ", minimo=1)
                if idx is None or idx > len(info["calificaciones"]):
                    print("Índice inválido.")
                else:
                    removed = info["calificaciones"].pop(idx - 1)
                    print(f"Eliminada calificación: {removed}")
        elif opt == 6:
            if not info["calificaciones"]:
                print("No tiene calificaciones.")
            else:
                print("Calificaciones:", info["calificaciones"])
        elif opt == 7:
            print("Saliendo del editor.")
            return
        else:
            print("Opción inválida en el editor.")


def anadir_calificacion_rapida(estudiantes):
    print("\n--- Añadir calificación rápida ---")
    id_ = pedir_texto("ID del estudiante: ")
    if id_ is None:
        return
    if id_ not in estudiantes:
        print("ID no encontrada.")
        return
    val_raw = pedir_texto("Calificación a añadir (0-100): ")
    if val_raw is None:
        return
    try:
        val = float(val_raw)
    except ValueError:
        print("Calificación inválida.")
        return
    if val < 0 or val > 100:
        print("Calificación fuera de rango.")
        return
    estudiantes[id_]["calificaciones"].append(val)
    print(f"Calificación {val} añadida a {id_} - {estudiantes[id_]['nombre']}")


# -------------------------
# Búsqueda por nombre parcial
# -------------------------
def buscar_por_nombre(estudiantes):
    print("\n--- Buscar por nombre parcial ---")
    q = pedir_texto("Escribe parte del nombre a buscar: ")
    if q is None:
        return
    q = q.lower()
    resultados = []
    for id_, info in estudiantes.items():
        if q in info["nombre"].lower():
            resultados.append((id_, info))
    if not resultados:
        print("No se encontraron coincidencias.")
        return
    print(f"Se encontraron {len(resultados)} coincidencia(s):")
    for id_, info in resultados:
        prom = calcular_promedio(info["calificaciones"])
        prom_text = f"{prom:.2f}" if prom is not None else "N/A"
        print(f"{id_} - {info['nombre']} - Edad: {info['edad']} - Promedio: {prom_text}")


# -------------------------
# Estadísticas del grupo
# -------------------------
def estadisticas_grupo(estudiantes):
    print("\n--- Estadísticas del grupo ---")
    if not estudiantes:
        print("No hay datos para calcular estadísticas.")
        return
    todas_califs = []
    for id_, info in estudiantes.items():
        todas_califs.extend([(id_, val) for val in info["calificaciones"]])
    if not todas_califs:
        print("No hay calificaciones registradas.")
        return
    # promedio general
    valores = [val for (_id, val) in todas_califs]
    promedio_general = sum(valores) / len(valores)
    max_val = max(valores)
    min_val = min(valores)
    # estudiantes con nota max/min
    estudiantes_max = sorted({id_ for (id_, v) in todas_califs if v == max_val})
    estudiantes_min = sorted({id_ for (id_, v) in todas_califs if v == min_val})
    # mejor promedio por estudiante
    mejores = []
    mejor_prom = -1
    for id_, info in estudiantes.items():
        prom = calcular_promedio(info["calificaciones"])
        if prom is None:
            continue
        if prom > mejor_prom:
            mejor_prom = prom
            mejores = [id_]
        elif prom == mejor_prom:
            mejores.append(id_)
    print(f"Promedio general del grupo: {promedio_general:.2f}")
    print(f"Máxima calificación: {max_val} (estudiante(s): {', '.join(estudiantes_max)})")
    print(f"Mínima calificación: {min_val} (estudiante(s): {', '.join(estudiantes_min)})")
    if mejores:
        print(f"Mejor promedio: {mejor_prom:.2f} (estudiante(s): {', '.join(mejores)})")
    else:
        print("No hay promedios calculables por falta de calificaciones por estudiante.")


# -------------------------
# Menú principal
# -------------------------
def menu():
    estudiantes = {}
    if os.path.exists(FILENAME):
        print(f"Se encontró '{FILENAME}'. ¿Deseas cargar los estudiantes guardados? (s/n)")
        if input("> ").strip().lower() == "s":
            estudiantes = cargar_desde_archivo()
            print(f"Cargados {len(estudiantes)} estudiantes.")

    while True:
        print("\n=== Gestor de Estudiantes (Mejorado) ===")
        print("1) Agregar nuevo estudiante")
        print("2) Mostrar todos los estudiantes")
        print("3) Calcular promedio de un estudiante por ID")
        print("4) Añadir calificación rápida a un estudiante")
        print("5) Editar estudiante (nombre/edad/calificaciones)")
        print("6) Eliminar un estudiante")
        print("7) Buscar por nombre parcial")
        print("8) Estadísticas del grupo")
        print("9) Guardar en archivo")
        print("10) Cargar desde archivo (sobrescribe memoria actual)")
        print("11) Salir")
        opt = input("> ").strip()
        if opt == "1":
            agregar_estudiante(estudiantes)
        elif opt == "2":
            mostrar_todos(estudiantes)
        elif opt == "3":
            promedio_por_id(estudiantes)
        elif opt == "4":
            anadir_calificacion_rapida(estudiantes)
        elif opt == "5":
            editar_estudiante(estudiantes)
        elif opt == "6":
            eliminar_estudiante(estudiantes)
        elif opt == "7":
            buscar_por_nombre(estudiantes)
        elif opt == "8":
            estadisticas_grupo(estudiantes)
        elif opt == "9":
            guardar_en_archivo(estudiantes)
        elif opt == "10":
            confirm = input("Esto sobrescribirá los datos en memoria. ¿Continuar? (s/n): ").strip().lower()
            if confirm == "s":
                estudiantes = cargar_desde_archivo()
                print(f"Cargados {len(estudiantes)} estudiantes.")
            else:
                print("Carga cancelada.")
        elif opt == "11":
            print("Saliendo. ¿Deseas guardar antes de salir? (s/n)")
            if input("> ").strip().lower() == "s":
                guardar_en_archivo(estudiantes)
            print("Adiós.")
            break
        else:
            print("Opción inválida. Elige un número del menú (1-11).")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario. Saliendo...")
        sys.exit(0)