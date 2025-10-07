# Interfaces
from abc import ABC, abstractmethod

# =======================
# Patrón OBSERVER
# =======================
class IObservador(ABC):
    @abstractmethod
    def actualizar(self, mensaje: str):
        pass


class Notificacion:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, usuario):
        self._observadores.append(usuario)

    def eliminar_observador(self, usuario):
        self._observadores.remove(usuario)

    def notificar_observadores(self, mensaje: str):
        for usuario in self._observadores:
            usuario.actualizar(mensaje)


# =======================
# Clase Usuario (Observador)
# =======================
class Usuario(IObservador):
    def __init__(self, nombre, email, telefono):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def actualizar(self, mensaje: str):
        print(f"[{self.nombre}] Recibió notificación: {mensaje}")


# =======================
# Patrón FACTORY METHOD
# =======================
class INotificacion(ABC):
    @abstractmethod
    def enviar(self, mensaje: str):
        pass


class EmailNotificacion(INotificacion):
    def enviar(self, mensaje: str):
        print(f"Enviando Email: {mensaje}")


class SMSNotificacion(INotificacion):
    def enviar(self, mensaje: str):
        print(f"Enviando SMS: {mensaje}")


class PushNotificacion(INotificacion):
    def enviar(self, mensaje: str):
        print(f"Enviando Notificación Push: {mensaje}")


class NotificacionFactory:
    @staticmethod
    def crear_notificacion(tipo: str) -> INotificacion:
        if tipo == "email":
            return EmailNotificacion()
        elif tipo == "sms":
            return SMSNotificacion()
        elif tipo == "push":
            return PushNotificacion()
        else:
            raise ValueError("Tipo de notificación no soportado")


# =======================
# Simulación / Ejemplo de uso
# =======================
if __name__ == "__main__":
    # Crear usuarios
    usuario1 = Usuario("Ana", "ana@mail.com", "555-1234")
    usuario2 = Usuario("Luis", "luis@mail.com", "555-5678")

    # Crear sistema de notificaciones (Sujeto)
    sistema_notificaciones = Notificacion()

    # Suscribir usuarios
    sistema_notificaciones.agregar_observador(usuario1)
    sistema_notificaciones.agregar_observador(usuario2)

    # Crear notificaciones usando Factory
    fabrica = NotificacionFactory()
    notificacion_email = fabrica.crear_notificacion("email")
    notificacion_sms = fabrica.crear_notificacion("sms")

    # Enviar notificaciones
    mensaje = "Nueva actualización disponible"
    sistema_notificaciones.notificar_observadores(mensaje)

    # Usar las notificaciones creadas
    notificacion_email.enviar(mensaje)
    notificacion_sms.enviar(mensaje)
