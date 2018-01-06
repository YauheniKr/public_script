import telnetlib
import time
import getpass
import sys
#import socket добавилось
import socket

COMMAND = sys.argv[1].encode('utf-8')
USER = input('Username: ').encode('utf-8')
PASSWORD = getpass.getpass().encode('utf-8')
ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ').encode('utf-8')


#DEVICES_IP = ['192.168.100.1', '192.168.100.2', '192.168.100.3']
DEVICES_IP = ['192.168.100.1']

for IP in DEVICES_IP:
    print('Connection to device {}'.format(IP))
	#добавился timeout
    with telnetlib.Telnet(IP, timeout=5) as t:

        t.read_until(b'Username:')
        t.write(USER + b'\n')

        t.read_until(b'Password:')
        t.write(PASSWORD + b'\n')
        t.write(b'enable\n')

        t.read_until(b'Password:')
        t.write(ENABLE_PASS + b'\n')
        t.write(b'terminal length 0\n')

        time.sleep(1)
        t.read_very_eager()
        t.write(COMMAND + b'\n')
        data = b''
        while True:
			#тут вместо проверки приглашения, полагаемся на таймаут
			#соединения
			#если данных нет 5 сек, будет исключение
			#тогда и прерываем цикл
            try:
                part = t.read_some()
            except socket.timeout:
                break
            data += part
            #if b'#' in part:
            #    break
        print(data.decode('utf-8'))
