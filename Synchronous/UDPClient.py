import socket

addr = 'localhost', 8888

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 无socket.connect()

while True:
	data = input('What do you want to send?  ')
	socket.sendto(bytes(data, 'utf-8'), addr)

	socket.settimeout(1) # 设置时间期限为1s，防止Server出现错误无法发送数据
	received = socket.recv(1024) 

	print('received: ' + str(received, 'utf-8'))