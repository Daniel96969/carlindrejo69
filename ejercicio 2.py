#!/usr/bin/env python3
"""
Calculadora Matricial usando NumPy
Operaciones:
 - Suma (A + B)
 - Resta (A - B)
 - Multiplicación matricial (A @ B)
 - Transposición (A.T)
Menú interactivo; validación de dimensiones; permite múltiples operaciones.
Guardar este archivo como calc_matrices.py y ejecutar: python calc_matrices.py
"""

import sys

# Intentamos importar numpy y damos indicaciones si falla
try:
    import numpy as np
except Exception as e:
    print("ERROR: NumPy no está disponible.")
    print("Instálalo con: pip install numpy")
    sys.exit(1)

np.set_printoptions(precision=4, suppress=True)


def leer_entero(prompt, minimo=None):
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
            if minimo is not None and v < minimo:
                print(f"Introduce un número entero >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Entrada inválida. Escribe un número entero.")


def parsear_fila(s, cols):
    # acepta separación por espacios o coma
    partes = [p for p in s.replace(",", " ").split() if p != ""]
    if len(partes) != cols:
        raise ValueError(f"Se esperaban {cols} valores, pero se recibieron {len(partes)}.")
    try:
        return [float(x) for x in partes]
    except ValueError:
        raise ValueError("Todos los elementos deben ser números (enteros o decimales).")


def leer_matriz(nombre="M"):
    print(f"\n--- Entrada de la matriz {nombre} ---")
    filas = leer_entero("Número de filas: ", minimo=1)
    cols = leer_entero("Número de columnas: ", minimo=1)
    datos = []
    print("Introduce cada fila como valores separados por espacios o comas.")
    for i in range(filas):
        while True:
            s = input(f"Fila {i+1} (ej: 1 2 3): ").strip()
            try:
                fila = parsear_fila(s, cols)
                datos.append(fila)
                break
            except ValueError as err:
                print("Error:", err)
                print("Intenta de nuevo.")
    mat = np.array(datos, dtype=float)
    print(f"Matriz {nombre} leída ({filas}x{cols}):\n{mat}")
    return mat


def mostrar_matriz(mat, nombre="M"):
    print(f"\n{nombre} ({mat.shape[0]}x{mat.shape[1]}):")
    print(mat)


def menu_principal():
    print("=== Calculadora Matricial (NumPy) ===")


def operaciones_matriciales():
    A = None
    B = None

    while True:
        menu_principal()
        print("""
Menú:
1) Ingresar/crear matriz A
2) Ingresar/crear matriz B
3) Mostrar matrices actuales
4) Suma (A + B)
5) Resta (A - B)
6) Multiplicación matricial (A @ B)
7) Transposición (A.T) - elige A o B
8) Reingresar matrices (limpiar)
9) Salir
""")
        opt = input("> ").strip()

        if opt == "1":
            A = leer_matriz("A")
        elif opt == "2":
            B = leer_matriz("B")
        elif opt == "3":
            if A is None:
                print("\nA: (no definida)")
            else:
                mostrar_matriz(A, "A")
            if B is None:
                print("\nB: (no definida)")
            else:
                mostrar_matriz(B, "B")
        elif opt == "4":
            # Suma: mismas dimensiones
            if A is None or B is None:
                print("Define ambas matrices A y B antes de operar.")
                continue
            if A.shape != B.shape:
                print(f"No son compatibles para suma: formas A{A.shape} != B{B.shape}")
                continue
            C = A + B
            print("\nResultado (A + B):")
            print(C)
        elif opt == "5":
            # Resta
            if A is None or B is None:
                print("Define ambas matrices A y B antes de operar.")
                continue
            if A.shape != B.shape:
                print(f"No son compatibles para resta: formas A{A.shape} != B{B.shape}")
                continue
            C = A - B
            print("\nResultado (A - B):")
            print(C)
        elif opt == "6":
            # Multiplicación matricial
            if A is None or B is None:
                print("Define ambas matrices A y B antes de operar.")
                continue
            if A.shape[1] != B.shape[0]:
                print(f"No son compatibles para multiplicación matricial: A columnas {A.shape[1]} != B filas {B.shape[0]}")
                continue
            C = A @ B  # o np.dot(A,B)
            print("\nResultado (A @ B):")
            print(C)
        elif opt == "7":
            if A is None and B is None:
                print("No hay matrices definidas para transponer.")
                continue
            selector = input("Transponer cuál? (A/B): ").strip().upper()
            if selector == "A":
                if A is None:
                    print("A no está definida.")
                    continue
                print("\nA.T:")
                print(A.T)
            elif selector == "B":
                if B is None:
                    print("B no está definida.")
                    continue
                print("\nB.T:")
                print(B.T)
            else:
                print("Opción inválida.")
        elif opt == "8":
            A = None
            B = None
            print("Matrices limpiadas.")
        elif opt == "9":
            print("Saliendo. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Elige un número del menú.")


if __name__ == "__main__":
    operaciones_matriciales()
