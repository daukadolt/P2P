import socket


def download_from_peer(peer_host, peer_port, file_name, file_type, file_size):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_host, peer_port))
        file_request_message = 'DOWNLOAD: {file_name}, {file_type}, {file_size}'.format(
            file_name=file_name, file_type=file_type, file_size=file_size
        )
        file_request_message = file_request_message.encode()
        s.sendall(file_request_message)
        buffer_size = 1024
        file_data = s.recv(buffer_size)
        more_bytes_to_come = len(file_data) == 1024
        file_data = file_data[6:]  # omitting 'FILE: '
        if more_bytes_to_come:
            while True:
                buffer = s.recv(buffer_size)
                file_data += buffer
                if len(buffer) < buffer_size: break

        with open('./{}'.format(file_name), 'wb') as output_file:
            output_file.write(file_data)


if __name__ == '__main__':
    print('peer host, peer port, file_name, file_type, file_size: ')
    peer_host, peer_port, file_name, file_type, file_size = input().split()
    peer_port = int(peer_port)
    file_size = float(file_size)
    download_from_peer(peer_host, peer_port, file_name, file_type, file_size)