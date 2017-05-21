# 学习自博客: http://blog.csdn.net/songfreeman/article/details/51179213

import socket
import queue
import select

# 用线程的IO多路复用实现一个读写分离的、支持多客户端的连接请求  
def SelectServer(Server_addr):
	server = socket.socket()

	server.bind(Server_addr)
	server.listen(10)

	server.setblocking(False)  # 设置非阻塞，即异步

	message_queue = {}  # client socket的消息队列
	input_list = []   # 等待接受信息的client socket
	output_list = []  # 等待发送的client socket

	input_list.append(server)

	while True:
		stdinput, stdoutput, stderr  = select.select(input_list, output_list, input_list)
		# stdinput, stdoutput, stderr 分别是 input_list, output_list, input_list 的子集

		for obj in stdinput: # 查看所有要输入的file description
			if obj == server: # 如果是服务器监听端口有响应, 那就是有客户端请求连接
				client_socket, client_addr = server.accept() # 接受client socket (第三次握手)
				print('Client {} connected!'.format(client_addr))

				input_list.append(client_socket) # 要接受client socket的信息，放入input_list 队列
				message_queue[client_socket] = queue.Queue() # 开辟一个队列空间

			else:
				try: # obj is Client's socket, 可能client socket会发送数据过来，准备接受(也可能不发送数据)
					client_data = obj.recv(1024)

					if client_data: # 接受到了数据
						print('Received {} from client {}'.format(client_data, obj.getpeername())) # obj.getpeername() 获得socket的 (ip, port)

						message_queue[obj].put(client_data) # 放入该客户端的数据

						if obj not in output_list: # 接下来准备发送数据给 client socket， 要放入output_list 
							output_list.append(obj) 

				except ConnectionResetError:
					# client's socket is closed
					# 清理该用户的数据
					input_list.remove(obj) # input_list中移除
					del message_queue[obj] 
					print('[input] Client {} disconnected'.format(obj.getpeername()))

		for send_obj in output_list: # 准备发送数据
			try:
				if not message_queue[send_obj].empty():  # 读取给用户发送的 message
					send_data = message_queue[send_obj].get() 
					send_obj.sendall(send_data)


			except ConnectionResetError :
				# 用户的链接已经关闭，清理用户的数据
				del message_queue[send_obj]
				output_list.remove(send_obj)
				print('[output] client {} disconnected'.format(send_obj.getpeername()))

		for err_obj in stderr:
			print('Exception condition on', err_obj.getpeername())
			# 清除用户数据
			input_list.remove(err_obj)
			try:
				output_list.remove(err_obj)
			except:
				pass

			err_obj.close()

			del message_queue[err_obj] 




if __name__ == '__main__':
	addr = '', 8888
	SelectServer(addr)