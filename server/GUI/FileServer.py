import socket, os
import threading, logging
from File import File

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO,
                    datefmt='%H:%M:%S')


class FileServer:
    def __init__(self, self_host='127.0.0.1'):
        self.shared_files = {}
        self.host = self_host
        self.port = 0
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.bind((self.host, self.port))
        self.port = self.main_socket.getsockname()[1]

    def start(self, ft_host, ft_port):
        def read_files():
            path_to_files = './files'
            for filename in os.listdir(path_to_files):
                self.shared_files[filename] = File('{}/{}'.format(path_to_files, filename))

        def format_shared_files(host_ip, host_port):
            # assuming shared_files is a dictionary
            formatted_with_host_port = []
            for file in self.shared_files.values():
                formatted_with_host_port.append(file.format_for_sending(host_ip, host_port))
            text = ', '.join(formatted_with_host_port)
            return text.encode()

        def connect_to_ft():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ft_host, ft_port))
                s.send(b'HELLO')
                data = s.recv(1024)
                if data != b'HI': raise BaseException
                payload = format_shared_files(self.host, self.port)
                s.sendall(payload)

        def file_server_listen():

            def process_file_request(peer_sock, peer_addr):
                data = peer_sock.recv(1024)
                decoded = data.decode()
                if not isinstance(decoded, str): raise BaseException
                if decoded.split(':')[0] == 'DOWNLOAD':
                    file_data = decoded.split(':')[1]
                    file_data = file_data.strip()
                    logging.info(file_data)
                    file_name, file_type, size = [string.strip() for string in file_data.split(',')]
                    if file_name not in self.shared_files:
                        return peer_sock.close()
                    with open(self.shared_files[file_name].path, 'rb') as file_bytes:
                        peer_sock.sendall(b'FILE: ' + file_bytes.read())
                        peer_sock.close()

            print('file_server_listen started')
            main_socket = self.main_socket

            main_socket.listen()
            while True:
                conn, addr = main_socket.accept()
                file_request = threading.Thread(target=process_file_request, args=(conn, addr))
                file_request.start()

        read_files()

        connect_to_ft()

        peer_listener = threading.Thread(target=file_server_listen)
        peer_listener.start()
        logging.info('threaded file_server_listener')


if __name__ == '__main__':
    ft_port = int(input())
    server = FileServer()
    server.start('127.0.0.1', ft_port)
