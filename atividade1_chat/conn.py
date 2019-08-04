import socket
import struct
import flag
import subprocess
import pickle
import random

class Conn():
    def __init__(self, group):
        self.name = ''
        self.group = group
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        self.reserved = ['1000', '1001', '1004', '1044', '2000',
                         '2244', '4441', '4422', '4444', '9000',
                         '9991','9992','9992','9999']
        self.people = []
        self.dispute = []
        self.ip = subprocess.getoutput("hostname -I | cut -f1 -d \" \" ")
        self.master = False
        self.Loose = False
        self.master_addr = ''
        self.contest = 0

    def newChating(self, info, data):
        # Nova pessoa no chat

        user, addr = info
        msg = data[1]
        dic = ''
        if len(data) > 2:
            dic = data[2]

        # Mensagens recebidas pelo mestre
        if self.master and self.ip != addr:
            # Alguem mundou msg perguntando quem é o mestre
            if msg == '1000':

                print('###1000 receive: Who is The Master?')
                # Mestre responde diretamente
                self.send_uni('9000', addr)
                print('###9000 send: I\'m The Master!')

            # Verifica Nome
            elif msg == '9991':
                print('###9991 receive: Abaout my name')
                if user in self.people:
                    self.send_uni('4444', addr)
                    print('###4444 send: Bad Name')
                else:
                    self.people.append(user)
                    self.send_uni('2000', addr)
                    print('###2000 send: Good Name!')

            # Lista de pessoas
            elif msg == '9992':
                print('###9992 receive: send List')
                people = ''.join(str(p)+'|' for p in self.people)
                self.send_mult('2244|'+people)
                print('###2244 send: List sent')
                flag.event.set()


        # Mensagens recebidas do mestre pela primeira vez
        elif msg == '9000' and self.ip != addr:
            print('###9000 receive: I\'m The Master!')
            self.master_addr = addr
            self.send_uni('9991', self.master_addr)

        # Mensagens recebidas do mestre
        elif self.master_addr == addr and self.ip != addr:

            # Nome ok
            if msg == '2000':
                print('###2000 receive: Good Name!')
                # Solicita Lista de pessoas
                self.send_uni('9992', addr)
                print('###9992 send: send List')

            # Nome fail
            elif msg == '4444':
                print('#4444 receive: Bad Name!')
                self.setName()

            # recebe lista
            elif msg == '2244':
                print('###2244 receive: List sent')
                for i in range(len(data)):
                    if i >= 2 and i < len(data):
                        print(data[i])
                        self.people.append(data[i])
                flag.event.set()

        # mensagem para decidir o mestre
        elif self.ip != addr and not self.Loose:
            '''
            if msg == '1000':
                pass

            elif msg == '1001':
                for i in range(len(self.people)):
                    if user in self.people[i]:
                        self.people.remove(i)
                        print('saiu')

            # Nome inserido invalido
            elif msg == '4444' and len(self.people) == 0:
                print('###4444 receive: choose other name')
                self.setName()

            # msg de outro com desejo de ingressar no chat
            elif msg == '1000' and self.name != '':
                pass
            '''

            # Disputa pelo mestre
            if msg == '1000':
                if not addr in self.dispute:
                    self.dispute.append(addr)
                self.contest = random.randint(0,999)
                print('###1000 receive: Who is The Master?')
                self.send_mult('1044|' + str(self.contest))
                print('###1044 send: I want to be The Master!')

            elif msg == '1044':
                print('###1044 recevie: I want to be The Master!')
                if self.contest < int(dic):
                    self.Loose = True
                    self.send_mult('1004')
                    print('###1004: I Loose!')
                else:
                    self.send_mult('1000')
                    print('###1000 send: Who is The Master!')

            elif msg == '1004':
                if len(self.dispute) > 1:
                    print('###1004 send: I Loose!')
                    self.dispute.remove(addr)
                else:

                    self.master = True
                    self.master_addr = self.ip
                    self.people.append(self.name)
                    self.send_mult('9000')
                    self.dispute.clear()
                    print('###9000 send: I\'m The Master!')
                    flag.event.set()


    def send_mult(self, msg):
        data = self.name+"|"+msg
        self.sock.sendto(data.encode(), self.group)

    def send_uni(self, msg, addr):
        data = self.name + "|" + msg
        self.sock.sendto(data.encode(), (addr, 48881))

    def recv(self):
        self.sock.bind(('', 48881))
        group = socket.inet_aton(self.group[0])
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            recv, addr = self.sock.recvfrom(1024)
            with flag.lock:
                data = recv.decode().split("|")
                user = data[0]
                if data[1] in self.reserved:
                    self.newChating((user, addr[0]), data)
                else:
                    id = '[' + user + '] >>'
                    print(id, data[1])

    def setName(self):
        self.name = input('Nome: ')
        self.send_mult('9991')
        print('###9000 send: I\'m The Master!')

    def serchMaster(self):
        self.name = input('Nome: ')
        self.send_mult('1000')
        print('###1000 send: Who is The Master!')

    def getName(self):
        return self.name
