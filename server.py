import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server started on", HOST, "port", PORT)

clients = {}
topics = {}  # topic_name: list of clients


def broadcast(message, topic, sender_conn):
    for client in topics.get(topic, []):
        if client != sender_conn:
            try:
                client.send(message)
            except:
                topics[topic].remove(client)


def handle_client(conn, addr):
    print(f"New connection from {addr}")
    conn.send("Enter topic to join or create: ".encode())
    topic = conn.recv(1024).decode().strip()

    if topic not in topics:
        topics[topic] = []

    topics[topic].append(conn)
    clients[conn] = topic

    conn.send(f"Joined topic: {topic}\n".encode())

    while True:
        try:
            msg = conn.recv(1024)
            if msg:
                broadcast(f"[{addr}] {msg.decode()}".encode(), topic, conn)
        except:
            topics[topic].remove(conn)
            del clients[conn]
            conn.close()
            break


while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
