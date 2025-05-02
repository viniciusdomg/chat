import grpc
from concurrent import futures
import time
import threading

import chat_pb2
import chat_pb2_grpc
from queueWriter import QueueWriter

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = []  # Lista de streams abertos (clientes conectados)
        self.lock = threading.Lock()  # Para evitar concorrência ao acessar self.clients

    def SendMessage(self, request, context):
        print(f"[{request.username}] {request.message}")

        with self.lock:
            for client in self.clients:
                try:
                    client.write(request)
                except:
                    pass
        return chat_pb2.Empty()

    def ReceiveMessages(self, request, context):
        # Cria um canal para enviar mensagens para este cliente
        queue = QueueWriter()
        with self.lock:
            self.clients.append(queue)

        try:
            while True:
                msg = queue.read()
                yield msg
        except:
            pass
        finally:
            with self.lock:
                self.clients.remove(queue)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051') # insecure_port é importante para testes locais sem autenticação
    server.start()
    print("Servidor iniciado na porta 50051")
    try:
        while True:
            time.sleep(86400)  # Mantém o servidor vivo
    except KeyboardInterrupt:
        print("Encerrando servidor...")
        server.stop(0)

if __name__ == '__main__':
    serve()
