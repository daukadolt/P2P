import unittest
import socket
from Server import Server
HOST = '127.0.0.1'
PORT = 37864

class TestServerMethods(unittest.TestCase):    
    def test_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
            cli.connect((HOST, PORT))
            cli.send(b'HELLO')
            data = cli.recv(1024)
            self.assertEqual(data, b'HI')
            cli.send(b'<mashina, filetype, 51235, date, ip address, port>, <ural, pdf, filesize, date, ip address, port>')
            cli.close()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
            cli.connect((HOST, PORT))
            cli.send(b'SEARCH:ural')
            data = cli.recv(1024)
            data = data.decode()
            print(data)
            cli.close()
    
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # Проверим, что s.split не работает, если разделитель - не строка
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
