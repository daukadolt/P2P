import socket
import multiprocessing


activePeerAddresses = []
fileList = {}
#creates val from data (according to the format)
def createVal(data):
    res = "<"
    for x in range(1, len(data)-1):
        val = data[x].strip()
        res += val + ","
    res += data[len(data)-1].strip()+ ">"
    return res

def handle(connection, address):
    data = connection.recv(1024)

    if(data == b'HELLO'):
        connection.send(b'HI')
        data = connection.recv(1024)
        # here data represented as list of files in the cleint
        if data:
            data = data.decode()
            data = data.split('>,')
            
            for x in data: 
                x = x.strip('< >')
                x = x.split(',')
                key = x[0] #filename 
                value = createVal(x) #value
                if(key in fileList):
                    fileList[key].append(value)
                else:
                    fileList[key] = [value]

            print(fileList)
            pass
            
    connection.close()
    

class Server:
    def __init__(self, host='127.0.0.1', port=None):
        if port is None:
            port = 37863
        self.host = host
        self.port = port

    def start(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.port = self.socket.getsockname()[1]
        self.socket.listen()
        # start of the process
        while(True):
            conn, addr = self.socket.accept()
            process = multiprocessing.Process(target=handle, args=(conn, addr))
            process.daemon = True
            process.start()

if __name__ == '__main__':
    s = Server()
    print(s.port)
    s.start()

#           while(True):
#             conn, addr = self.socket.accept()
#             data = conn.recv(1024)
#             if not data:
#                 break
#             if(data == b'HELLO'):
#                 conn.send(b'HI')
#                 data = conn.recv(1024)
#                 if(data == b'SEARCH'):
#                     # here we should check if it is in our active list
#                     print('search file name')
#                     conn.send(b'here i send list')
#                 # expect file formats and enter it to the list
#                 conn.close()
#             else:
#                 print('Bad handshake')
#                 conn.close()
