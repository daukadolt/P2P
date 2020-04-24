import socket


def search(ft_host, ft_port, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ft_host, ft_port))
        search_request = 'SEARCH: {}'.format(filename)
        search_request = search_request.encode()
        s.sendall(search_request)
        data = s.recv(1024)
        print(data)


if __name__ == '__main__':
    print('ft_port, ft_port, filename: ', end='')
    host, port, file_name = input().split()
    port = int(port)
    search(host, port, file_name)
