from tkinter import *
from tkinter import messagebox
import time
import os
from FileServer import FileServer
import FileDownloader
import socket

global_data = {'ft_host': None, 'ft_port': None}

root = Tk()
root.geometry('400x400')

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

search_file = Entry(root, width = 25, border = 5) #to get input
search_file.pack()

listBox = Listbox(root, width = 65)
listBox.pack()

scrollbar.config(command=listBox.yview)
listBox.config(yscrollcommand=scrollbar.set)



def searchClick():
	#here I send request to server and get list of files
	listBox.delete(0, END)
	searchText = search_file.get()
	files = getFilesFromServer(searchText)
	for file in files:
		listBox.insert(END, file)

def getFilesFromServer(filename):
	results = []
	ft_host, ft_port = global_data['ft_host'], global_data['ft_port']
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((ft_host, ft_port))
		search_request = 'SEARCH: {}'.format(filename)
		search_request = search_request.encode()
		s.sendall(search_request)
		data = s.recv(1024)
		data = data.decode()
		if data == 'NOT FOUND': return ['NOT FOUND']
		files = data.split('FOUND:')[-1]
		files = files.strip()
		if len(files) != 1:
			files = files.split('>, ')
			for file in files:
				file = file.strip('<>')
				results.append('<{}>'.format(file))
	return results

def getIpAndPortFromItem(item):
	item = item.strip('<>')
	details = item.split(',')
	return details[-2], details[-1]

def downloadFileFrom(ip, port):
	label = Label(root, text='Downloading File')
	label.pack()
	filename = search_file.get().strip()
	FileDownloader.download_from_peer(ip, int(port), filename, 'whatever', 123)
	#here you download and save the file
	label.after(1500, label.destroy)

def dbClickOnListItem(event):
	item = listBox.get('active')
	print('event', event)
	ip, port = getIpAndPortFromItem(item)
	print(ip, port)
	downloadFileFrom(ip, port)

def onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #send bye to the ft server
        print("BYE!")
        time.sleep(1)
        root.destroy()

def sendFileInfoToServer():
	time.sleep(1)
	for file_name in os.listdir('./files'):
		print('sending', file_name)
	fs = FileServer()
	print('FT server ip: ', end=" ")
	ft_host = input()
	global_data['ft_host'] = ft_host
	print('FT server port: ', end=" ")
	ft_port = int(input())
	global_data['ft_port'] = ft_port
	print('connecting to FT...')
	fs.start(ft_host, ft_port)
	print('Send files to server and get response')


listBox.bind('<Double-1>', dbClickOnListItem)
button = Button(root, text = "Search", command = searchClick)
button.pack()
root.after_idle(sendFileInfoToServer) # handler on start, to send files automatically
root.protocol("WM_DELETE_WINDOW", onClosing) # handler that starts when close clicked
root.mainloop()