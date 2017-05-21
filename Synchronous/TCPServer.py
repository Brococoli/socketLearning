import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
	"""docstring for MyTCPHandler"""
	

	def setup(self):
		print('Prapare to exchange data!')

	def handle(self):
		socket = self.request
		print('connecting from ' , self.client_address)
		self.data = str(socket.recv(1024),'utf-8')

		if(self.data == 'exit'):
			print('close connection!')
			return
		else:
			print('recv: ' + self.data)
			socket.sendall(bytes('you send: ' + self.data, 'utf-8'))
			print('Have sended!')

	def finish(self):
		print('Finish connection!')

if __name__ == '__main__':
	host = ''
	port = 8888
	addr = host,port
	server = socketserver.TCPServer(addr, MyTCPHandler)
	server.serve_forever()

