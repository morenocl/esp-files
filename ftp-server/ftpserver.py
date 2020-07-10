import usocket
from connection import Connection
import network
import gc


class Server:

    def __init__(self):
        wlan = network.WLAN()
        self.ip = wlan.ifconfig()[0]
        self.s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        self.s.bind((self.ip, 21))

    def serve(self):
        self.s.listen(1)
        print('Running: %s:%d' % (self.ip, 21))
        while True:
            cliente, addCliente = self.s.accept()
            conexion = Connection(cliente)
            while conexion.is_connected:
                conexion.handle()
                gc.collect()
