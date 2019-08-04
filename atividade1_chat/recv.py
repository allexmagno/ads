import socket
import threading
import struct
from conn import *
'''
def com(data):
    return data.decode().split("|")

def recive(sock, server):
    sock.bind(server)
    #group = socket.inet_aton('239.0.10.11')
    group = socket.inet_aton('239.0.0.10')
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        recv, addr = sock.recvfrom(1024)
        user, msg = com(recv)
        id = '['+user+'] >>'
        print(id, msg, addr)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ('',48881)
recv_msg = threading.Thread(target=recive, args=(sock, server))
recv_msg.start()
'''
group = ('239.0.0.10', 48881)
name = input('Nome: ')
conn = Conn(name, group)
conn.recv()