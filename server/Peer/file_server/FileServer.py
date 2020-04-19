import socket, os
from File import File


class FileServer:
    def __init__(self):
        self.shared_files = {}

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

        read_files()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ft_host, ft_port))
            s.send(b'HELLO')
            data = s.recv(1024)
            if data != b'HI': raise BaseException
            payload = format_shared_files(ft_host, ft_port)
            s.sendall(payload)
