import grpc
import threading

import chat_pb2
import chat_pb2_grpc

def receive_messages(stub, username):
    request = chat_pb2.Client(username=username)
    for message in stub.ReceiveMessages(request):
        print(f"\n[{message.username}] {message.message}")

def send_messages(stub, username):
    while True:
        msg = input()
        if msg.strip().lower() in ["sair", "exit", "quit"]:
            print("Encerrando chat...")
            break
        stub.SendMessage(chat_pb2.ChatMessage(username=username, message=msg))

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    username = input("Digite seu nome de usuário: ").strip()

    # Thread para receber mensagens
    t = threading.Thread(target=receive_messages, args=(stub, username), daemon=True)
    t.start()

    # Loop principal de envio
    send_messages(stub, username)

if __name__ == '__main__':
    main()
