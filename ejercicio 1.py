import random

def jugar():
    secreto = random.randint(1, 10)
    intentos = 0
    print("Adivina un número del 1 al 10")

    while True:
        intentos += 1
        try:
            n = int(input("Tu número: "))
        except ValueError:
            print("Ingresa un número entero válido.")
            continue

        if n == secreto:
            print(f"¡Correcto! Lo lograste en {intentos} intentos.")
            break
        elif n < secreto:
            print("Muy bajo.")
        else:
            print("Muy alto.")

if __name__ == "__main__":
    jugar()
