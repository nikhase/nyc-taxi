import socket
import streamer as streamerbsp



class listener:
    flag=1
    def __init__(self,ip,port):
        self._port=port
        self._ip=ip





    def start(self):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((self._ip, self._port))
        while listener.flag==1:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            return "received message:", data
        return "ENDE"