import threading
import socketserver
from ThreadedTCPClient import client

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		client_socket = self.request
		print('connected from ', self.client_address)
		print('Thread:', threading.enumerate())

		data = client_socket.recv(1024)
		print('receive: ' + str(data, 'utf-8'))

		cur_thread = threading.current_thread()
		response = bytes(cur_thread.name + ' : ', 'utf-8') + data
		client_socket.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): 
	""" 继承 ThreadingMixIn 和 TCPServer 便是TCP多线程服务器, 注意: 也是同步的，只不过是开了线程并行处理 """
	pass

if __name__ == '__main__':
	addr = 'localhost', 8888
	server = ThreadedTCPServer(addr, ThreadedTCPRequestHandler)

	# No.1
	server.serve_forever() # 将停在这里，一直处理进程

	""" No.2 官网写法 

	 with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever) 
		# 另开一个 serve_forever() 子线程，这样MainThread 可以直接运行下去

        # Exit the server thread when the main thread terminates

        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        client(ip, port, "Hello World 1")
        client(ip, port, "Hello World 2")
        client(ip, port, "Hello World 3")

        server.shutdown()

	
	"""


