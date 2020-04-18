import socket

HOST = '127.0.0.1'
port = 55456

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

sock.bind((HOST, port))

sock.listen()

while True:
    conn, addr = sock.accept()
    with conn:
        while True:
            print('connected to by', addr)
            data = conn.recv(1024)
            print(data)
            if not data:
                break