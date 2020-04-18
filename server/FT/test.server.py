import unittest
import socket
from Server import Server
HOST = '127.0.0.1'
PORT = 37863

class TestServerMethods(unittest.TestCase):    
    def test_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
            cli.connect((HOST, PORT))
            cli.send(b'HELLO')
            data = cli.recv(1024)
            cli.send(b'<filename, filetype, filesize, date, ip address, port>, <filename, filetype, filesize, date, ip address, port>')
            cli.close()
            self.assertEqual(data, b'HI')
            
    
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
