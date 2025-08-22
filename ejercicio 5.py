#!/usr/bin/env python3
"""
Ejercicio 19 - Manejo de archivos (versión mejorada)
- Lee estudiantes.txt con líneas "Nombre,Nota"
- Acepta notas con punto o coma decimal (ej. 85.5 o 85,5)
- Calcula promedio, mínimo y máximo de las notas válidas
- Genera reporte.txt con contenido original + estadísticas y listado de líneas ignoradas
- Manejo de errores (archivo no existe, formato inválido)
- Permite agregar nuevos estudiantes desde el programa (acepta coma decimal)
"""

import os
import sys

INPUT_FILE = "estudiantes.txt"
REPORT_FILE = "reporte.txt"


# -------------------------
# Lectura y parsing
# -------------------------
def normalizar_numero(s: str):
    """Normaliza un string numérico aceptando coma o punto como separador decimal."""
    if s is None:
        return None
    s = s.strip()
    # Reemplazar coma decimal por punto (pero no eliminar comas internas en nombres — aquí s es sólo la parte de la nota)
    s = s.replace(",", ".")
    return s


def leer_estudiantes(ruta):
    """
    Lee el archivo y devuelve:
      - validos: lista de tuplas (nombre:str, nota:float)
      - errores: lista de strings describiendo la línea inválida
      - raw_lines: lista de todas las líneas originales (sin newline)
    """
    validos = []
    errores = []
    raw_lines = []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for i, linea in enumerate(f, start=1):
                linea_orig = linea.rstrip("\n")
                raw_lines.append(linea_orig)
                linea = linea.strip()
                if not linea:
                    # conservar líneas vacías en raw_lines pero no contarlas como error
                    continue
                # separar por la primera coma: "Nombre,Nota" (si el nombre contiene comas, esto falla; asumimos formato simple)
                if "," not in linea:
                    errores.append(f"L{ i }: separador ',' no encontrado -> '{linea_orig}'")
                    continue
                nombre, nota_str = map(str.strip, linea.split(",", 1))
                if not nombre:
                    errores.append(f"L{ i }: nombre vacío -> '{linea_orig}'")
                    continue
                nota_norm = normalizar_numero(nota_str)
                try:
                    nota = float(nota_norm)
                    # validar rango típico 0-100 (se puede ajustar)
                    if nota < 0 or nota > 100:
                        errores.append(f"L{ i }: nota fuera de rango 0-100 -> '{linea_orig}'")
                        continue
                    validos.append((nombre, nota))
                except (ValueError, TypeError):
                    errores.append(f"L{ i }: nota no numérica -> '{linea_orig}'")
    except FileNotFoundError:
        raise
    return validos, errores, raw_lines


def calcular_promedio(validos):
    if not validos:
        return None
    total = sum(nota for (_n, nota) in validos)
    return total / len(validos)


# -------------------------
# Generar reporte con estadísticas
# -------------------------
def generar_reporte(input_ruta=INPUT_FILE, output_ruta=REPORT_FILE):
    """
    Lee estudiantes.txt, calcula estadísticas y escribe reporte.txt con:
      - contenido original (tal cual)
      - líneas con estadísticas:
          Total de entradas: X
          Válidas: Y
          Inválidas: Z
          Promedio general: N.N
          Nota máxima: M.M
          Nota mínima: m.m
      - listado de líneas inválidas comentadas (prefijo '#')
    Devuelve (ok:bool, mensaje:str).
    """
    # Leer archivo original (si no existe, informar)
    try:
        validos, errores, raw = leer_estudiantes(input_ruta)
    except FileNotFoundError:
        return False, f"El archivo '{input_ruta}' no existe."

    total_entries = len(raw)
    valid_count = len(validos)
    invalid_count = len(errores)

    prom = calcular_promedio(validos)
    prom_text = f"{prom:.1f}" if prom is not None else "N/A"

    notas = [nota for (_n, nota) in validos]
    max_text = f"{max(notas):.1f}" if notas else "N/A"
    min_text = f"{min(notas):.1f}" if notas else "N/A"

    # Escribir reporte
    try:
        with open(output_ruta, "w", encoding="utf-8") as out:
            # Escribir contenido original tal cual (incluir incluso líneas vacías)
            if raw:
                for line in raw:
                    out.write(line + "\n")
                out.write("\n")
            # Escribir estadísticas
            out.write("=== Estadísticas ===\n")
            out.write(f"Total de entradas (líneas en archivo): {total_entries}\n")
            out.write(f"Entradas válidas: {valid_count}\n")
            out.write(f"Entradas inválidas/ignoradas: {invalid_count}\n")
            out.write(f"Promedio general: {prom_text}\n")
            out.write(f"Nota máxima: {max_text}\n")
            out.write(f"Nota mínima: {min_text}\n")
            out.write("\n")
            # Añadir detalle de líneas inválidas (si las hay)
            if errores:
                out.write("# Líneas ignoradas por formato inválido o rango:\n")
                for e in errores:
                    out.write(f"# {e}\n")
        return True, f"Reporte generado en '{output_ruta}'. Promedio: {prom_text}."
    except Exception as e:
        return False, f"Error escribiendo '{output_ruta}': {e}"


# -------------------------
# Añadir estudiante (acepta coma decimal)
# -------------------------
def agregar_estudiante(nombre, nota_raw, ruta=INPUT_FILE):
    """
    Añade una línea al final de estudiantes.txt en formato 'Nombre,Nota'.
    nota_raw puede contener coma decimal. Se normaliza a punto al guardar.
    """
    if nombre is None or nombre.strip() == "":
        return False, "Nombre vacío."
    nr = normalizar_numero(str(nota_raw))
    try:
        nota = float(nr)
    except (ValueError, TypeError):
        return False, "Nota inválida (no numérica)."
    if nota < 0 or nota > 100:
        return False, "Nota fuera de rango 0-100."
    # Guardar con punto decimal (coherente)
    linea = f"{nombre.strip()},{nota}"
    try:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
        return True, f"Estudiante agregado: {linea}"
    except Exception as e:
        return False, f"Error al escribir en '{ruta}': {e}"


# -------------------------
# Utilidad para mostrar en consola
# -------------------------
def mostrar_estudiantes_con_resumen(ruta=INPUT_FILE):
    try:
        validos, errores, _raw = leer_estudiantes(ruta)
    except FileNotFoundError:
        print(f"El archivo '{ruta}' no existe.")
        return
    if validos:
        print("\nEntradas válidas:")
        for nombre, nota in validos:
            print(f"- {nombre}: {nota}")
    else:
        print("\nNo hay entradas válidas.")
    if errores:
        print("\nAdvertencias (líneas ignoradas):")
        for e in errores:
            print(f"- {e}")
    prom = calcular_promedio(validos)
    if prom is None:
        print("\nPromedio general: N/A (no hay notas válidas).")
    else:
        print(f"\nPromedio general: {prom:.1f}")
    if validos:
        notas = [n for (_nm, n) in validos]
        print(f"Nota máxima: {max(notas):.1f}")
        print(f"Nota mínima: {min(notas):.1f}")


# -------------------------
# Crear archivo de ejemplo
# -------------------------
def crear_archivo_ejemplo(ruta=INPUT_FILE):
    ejemplo = [
        "Ana,90",
        "Jorge,75",
        "Laura,85",
        "Marta,88,5"  # nota con coma decimal; la línea en archivo tendrá coma extra en este ejemplo: cuidado: por formato simple, solo la primera coma separa nombre/nota
    ]
    # Nota: para un ejemplo correcto con coma decimal en la nota, el separador entre nombre y nota debe ser coma
    # y la nota debe usar coma decimal; esto creará ambigüedad si el nombre contiene comas.
    # Para evitar ambigüedad en el ejemplo, cambiamos Marta a "Marta" y nota "88.5" (guardamos con punto).
    ejemplo = [
        "Ana,90",
        "Jorge,75",
        "Laura,85",
        "Marta,88.5"
    ]
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(ejemplo) + "\n")
        return True, f"Archivo de ejemplo '{ruta}' creado con {len(ejemplo)} entradas."
    except Exception as e:
        return False, f"Error creando archivo de ejemplo: {e}"


# -------------------------
# Menú principal
# -------------------------
def menu():
    print("=== Ejercicio 19: Manejo de archivos (mejorado) ===")
    while True:
        print("\nOpciones:")
        print("1) Leer estudiantes.txt, mostrar entradas y generar reporte.txt (con estadísticas)")
        print("2) Agregar nuevo estudiante a estudiantes.txt (acepta coma decimal)")
        print("3) Crear archivo de ejemplo estudiantes.txt (sobrescribe)")
        print("4) Salir")
        opt = input("> ").strip()
        if opt == "1":
            if not os.path.exists(INPUT_FILE):
                print(f"'{INPUT_FILE}' no existe.")
                crear = input("¿Deseas crear un archivo de ejemplo? (s/n): ").strip().lower()
                if crear == "s":
                    ok, msg = crear_archivo_ejemplo(INPUT_FILE)
                    print(msg)
                else:
                    continue
            mostrar_estudiantes_con_resumen(INPUT_FILE)
            ok, msg = generar_reporte(INPUT_FILE, REPORT_FILE)
            print(msg)
        elif opt == "2":
            print("\nAñadir nuevo estudiante (formato: Nombre,Nota).")
            nombre = input("Nombre completo: ").strip()
            if not nombre:
                print("Nombre no puede estar vacío. Cancelado.")
                continue
            nota_s = input("Nota (0-100). Puedes usar coma o punto decimal (ej. 85,5): ").strip()
            ok, msg = agregar_estudiante(nombre, nota_s, INPUT_FILE)
            print(msg)
        elif opt == "3":
            if os.path.exists(INPUT_FILE):
                print(f"'{INPUT_FILE}' ya existe. Si sobrescribes se perderán los datos actuales.")
                confirmar = input("¿Sobrescribir con ejemplo? (s/n): ").strip().lower()
                if confirmar != "s":
                    print("Operación cancelada.")
                    continue
            ok, msg = crear_archivo_ejemplo(INPUT_FILE)
            print(msg)
        elif opt == "4":
            print("Saliendo. ¿Deseas generar el reporte final antes de salir? (s/n)")
            if input("> ").strip().lower() == "s":
                if os.path.exists(INPUT_FILE):
                    ok, msg = generar_reporte(INPUT_FILE, REPORT_FILE)
                    print(msg)
                else:
                    print(f"No existe '{INPUT_FILE}', no se puede generar reporte.")
            print("Adiós.")
            break
        else:
            print("Opción inválida. Elige 1-4.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario. Saliendo...")
        sys.exit(0)
