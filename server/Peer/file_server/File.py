import ntpath
import os


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class File:

    def __init__(self, path):
        self.filename = path_leaf(path)
        self.type = self.filename.split('.')[1]
        self.size = os.stat(path).st_size
        self.last_modified = os.stat(path).st_mtime
        self.path = path

    def __repr__(self):
        return '<{filename}, {type}, {size}, {last_modified}>'.format(
            filename=self.filename, type=self.type, size=self.size, last_modified=self.last_modified
        )

    def format_for_sending(self, host_ip, host_port):
        return '<{filename}, {type}, {size}, {last_modified}, {ip}, {port}>'.format(
            filename=self.filename, type=self.type, size=self.size, last_modified=self.last_modified,
            ip=host_ip, port=host_port
        )

if __name__ == '__main__':
    first_file = os.listdir('./files')[0]
    file = File('./files/{}'.format(first_file))
    print(file)