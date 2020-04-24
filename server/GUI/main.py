from tkinter import *
from tkinter import messagebox
import time
import sys

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

def getFilesFromServer(fileName):
	fileHash = {}
	fileHash['dauka'] = [
		'<pdf,333,07/07/2020,192.168.0.5,4444>',
		'<pdf,333,07/07/2020,192.168.0.5,4444>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>',
		'<txt,833,07/07/2020,192.169.0.5,4414>'
	]
	if fileName in fileHash:
		return fileHash[fileName]
	return ['NOT FOUND']

def getIpAndPortFromItem(item):
	item = item.strip('<>')
	details = item.split(',')
	return details[-2], details[-1]

def downloadFileFrom(ip, port):
	label = Label(root, text='Downloading File')
	label.pack()
	#here you download and save the file 
	label.after(1500, label.destroy)

def dbClickOnListItem(event):
	item = listBox.get('active')
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
	for i, arg in enumerate(sys.argv):
		if not i == 0: 
			print("sending: ",arg)	
	print('Send files to server and get response')


listBox.bind('<Double-1>', dbClickOnListItem)
button = Button(root, text = "Search", command = searchClick)
button.pack()
root.after_idle(sendFileInfoToServer) # handler on start, to send files automatically
root.protocol("WM_DELETE_WINDOW", onClosing) # handler that starts when close clicked
root.mainloop()