import socket
import multiprocessing

manager = multiprocessing.Manager()
fileDict = manager.dict()
activePeerAddresses = manager.list()
#creates val from data (according to the format)
def createVal(data):
    res = "<"
    for x in range(1, len(data)-1):
        val = data[x].strip()
        res += val + ","
    res += data[len(data)-1].strip()+ ">"
    return res

def handle(connection, address, lock, activePeerAddresses, fileList):
    data = connection.recv(1024)

    if data == b'BYE':
        lock.acquire()
        #may be we should consider removing from the dict also
        activePeerAddresses.remove(address)
        lock.release()
    elif data == b'HELLO':
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
                lock.acquire()
                if(key in fileList):
                    fileList[key].append(value)
                else:
                    fileList[key] = [value]
                lock.release()
            lock.acquire()
            activePeerAddresses.append(address)
            lock.release()
            print("added files:",fileList)
            print("added ip address", activePeerAddresses)
    elif data:
        data = data.decode()
        data = data.split(':')
        if data[0].strip() == 'SEARCH':
            print(fileList)
            lock.acquire()
            value = fileList[data[1].strip()]
            lock.release()
            if value:
                value = 'FOUND:' + value    
            else:   
                value = 'NOT FOUND'
            connection.send(bytes(value))

    connection.close()
    

class Server:
    def __init__(self, host='127.0.0.1', port=None):
        if port is None:
            port = 37864
        self.host = host
        self.port = port

    def start(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.port = self.socket.getsockname()[1]
        self.socket.listen()
        lock = multiprocessing.Lock() 
        # start of the process
        while(True):
            conn, addr = self.socket.accept()
            process = multiprocessing.Process(target=handle, args=(conn, addr, lock, activePeerAddresses, fileDict))
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
