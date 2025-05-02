import threading


# Classe auxiliar: fila simples para mensagens por cliente
class QueueWriter:
    def __init__(self):
        self.messages = []
        self.condition = threading.Condition()

    def write(self, message):
        with self.condition:
            self.messages.append(message)
            self.condition.notify()

    def read(self):
        with self.condition:
            while not self.messages:
                self.condition.wait()
            return self.messages.pop(0)
