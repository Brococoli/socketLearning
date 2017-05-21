import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
	"""docstring for MyUDPHandler"""
	
	def handle(self):
		data, client_socket = self.request
		print('connected from', self.client_address)
		print('recv: ' + str(data, 'utf-8'))
		
		client_socket.send(bytes('I reveive: ', 'utf-8') + data, self.client_address)

	def finish(self):
		print('connect close')

if __name__ == '__main__':
	addr = '', 8888
	with socketserver.UDPServer(addr, MyUDPHandler) as server:
		server.serve_forever()