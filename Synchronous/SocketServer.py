import socket                # also TCP
s = socket.socket()
host = '0.0.0.0'
port = 8000
s.bind((host,port))
s.listen(5)


while True:
                print('waiting for connection')
                c, addr = s.accept()
                print('Got connection from', addr)
                while True:
                                print('connected:',addr,' wating for recv data')
                                try:
                                                data = c.recv(1024)
                                except Exception as e:
                                                print(e)
                                                c.close()
                                                break;
                                if not data:
                                                print("no data, close connection")
                                                break;

                                with open('./data.txt','ab') as f:
                                        f.write(data+b'\n')
                                mass = 'you send me :'.encode('utf-8') + data
                                c.send(mass)
                                print(b'sended: '+mass)
                c.close()
s.close()
