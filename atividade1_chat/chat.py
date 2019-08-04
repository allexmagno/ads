from threading import Thread, Event
from conn import *
import flag
import time

def interface(conn):

    while True:
        try:
            opt = int(input('Enviar mensagem:\n(1) grupo\n(2) privado\n'))
            if opt == 1:
                msg = input()
                conn.send_mult(msg)
            elif opt == 2:
                pass


        except ValueError:
            pass
def ctrl_C(sig, frame):
    print('a')

'''
def com(data):
    return data.decode().split("|")

def recv(sock, server):
    sock.bind(server)
    group = socket.inet_aton('239.0.0.10')
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        try:
            recv, addr = sock.recvfrom(1024)
            user, msg = com(recv)
            id = '['+user+'] >>'
            print(id, msg)
        except socket.timeout:
            print('timeout')

def send(sock, user, group):
    msg = input('['+user+'] >> ')
    data = user+"|"+msg
    sock.sendto(data.encode(), group)


group = ('239.0.0.10',48881)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
server = ('', 48881)


name = input('Nome: ')

itf = threading.Thread(target=interface, args=(sock, name, group))
#itf.start()
#send_msg = threading.Thread(target=send, args=(sock, name, group))
#recv_msg = threading.Thread(target=recv(sock))
#recv_msg = threading.Thread(target=recv, args=(sock, server))

#send_msg.start()
#recv_msg.start()

'''
flag.init()
group = ('239.0.0.10', 48881)

conn = Conn(group)

recv = Thread(target=conn.recv)
recv.start()

time.sleep(0.1)
conn.serchMaster()

flag.event.wait()
itf = Thread(target=interface, args=(conn,))
itf.start()
#signal.signal(signal.SIGINT, ctrl_C)

