import socket
import struct
import threading

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
USERNAME = input("Enter your name: ")

def receive_messages():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))

    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, _ = sock.recvfrom(1024)
        print(data.decode())

def send_messages():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input()
        full_msg = f"{USERNAME}: {msg}"
        sock.sendto(full_msg.encode(), (MULTICAST_GROUP, PORT))

# Start threads
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()