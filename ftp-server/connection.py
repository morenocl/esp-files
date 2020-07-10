import usocket
import uos
from ubinascii import b2a_base64, a2b_base64


# Constantes:
DELIM = b'/'
EOL = b'\r\n'
CODE_OK = 0
BAD_EOL = 100
BAD_REQUEST = 101
INTERNAL_ERROR = 199
INVALID_COMMAND = 200
INVALID_ARGUMENTS = 201
FILE_NOT_FOUND = 202
BAD_OFFSET = 203

error_messages = {
    CODE_OK: b'OK',
    # 1xx: Errores fatales (no se pueden atender más pedidos)
    BAD_EOL: b'BAD EOL',
    BAD_REQUEST: b'BAD REQUEST',
    INTERNAL_ERROR: b'INTERNAL SERVER ERROR',
    # 2xx: Errores no fatales (no se pudo atender este pedido)
    INVALID_COMMAND: b'NO SUCH COMMAND',
    INVALID_ARGUMENTS: b'INVALID ARGUMENTS FOR COMMAND',
    FILE_NOT_FOUND: b'FILE NOT FOUND',
    BAD_OFFSET: b'OFFSET EXCEEDS FILE SIZE',
}

valid_commands = [
    b'get_metadata',
    b'get_slice',
    b'get_file_listing',
    b'quit'
]


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket):
        self.socket = socket
        self.directory = b'/data'
        self.package = b''
        self.is_connected = True

    def handle(self):
        self.package = self.package + self.socket.recv(1024)
        print('Request: %s' % str(self.package))
        while EOL in self.package:
            # En un mismo paquete puede recibir multiples commandos.
            request, self.package = self.package.split(EOL, 1)
            self.process(request)

    def process(self, request):
        if b'\n' in request:
            response = self.make_response(BAD_EOL)
            self.socket.send(response)
        else:
            s = request.split(b' ')
            n = len(s)
            if s[0] not in valid_commands:
                response = self.make_response(INVALID_COMMAND)
                self.socket.send(response)
            elif n == 1:
                if s[0] == b'get_file_listing':
                    print('get_file_listing')
                    self.get_file_listing()
                elif s[0] == b'quit':
                    print('quit')
                    self.quit()
                else:
                    response = self.make_response(INVALID_ARGUMENTS)
                    self.socket.send(response)
            elif n == 2:
                if s[0] == b'get_metadata':
                    print('get_metadata')
                    self.get_metadata(s[1])
                else:
                    response = self.make_response(INVALID_ARGUMENTS)
                    self.socket.send(response)
            elif n == 4:
                if s[0] == b'get_slice':
                    print('get_slice')
                    self.get_slice(s[1], s[2], s[3])
                else:
                    response = self.make_response(INVALID_ARGUMENTS)
                    self.socket.send(response)

    def get_file_listing(self):
        try:
            list = b''
            items = uos.listdir(self.directory)
            for nombre in items:
                # 46 is '.' in ASCII, ignore hidden files.
                if nombre[0] != 46:
                    list = list + nombre + EOL
            list = self.make_response(CODE_OK, list + EOL)
        except:
            print('Ocurrio una excepcion en get_file_listing')
            list = self.make_response(INTERNAL_ERROR)
        self.socket.send(list)

    def get_metadata(self, filename):
        try:
            path = DELIM.join([self.directory, filename])
            sizefile = uos.stat(path)[6]
            list = self.make_response(CODE_OK, str(sizefile).encode() + EOL)
        except ValueError:
            print('Ocurrio una excepcion en get_slice: ValueError')
            list = self.make_response(INVALID_ARGUMENTS)
        except OSError:
            print('Ocurrio una excepcion en get_slice: OSError')
            list = self.make_response(FILE_NOT_FOUND)
        except:
            print('Ocurrio una excepcion en get_slice')
            list = self.make_response(INTERNAL_ERROR)
        finally:
            self.socket.send(list)

    def get_slice(self, filename, OFFSET, SIZE):
        try:
            path = DELIM.join([self.directory, filename])
            offset, size = int(OFFSET), int(SIZE)
            size_file = uos.stat(path)[6]
            if(size_file < size + offset):
                response = self.make_response(BAD_OFFSET)
            else:
                file = open(path, 'rb')
                file.seek(offset)
                data = file.read(size)
                encoded = b2a_base64(data) + EOL
                response = self.make_response(CODE_OK, encoded)
        except ValueError:
            print('Ocurrio una excepcion en get_slice: ValueError')
            response = self.make_response(INVALID_ARGUMENTS)
        except OSError:
            print('Ocurrio una excepcion en get_slice: OSError')
            response = self.make_response(FILE_NOT_FOUND)
        except:
            print('Ocurrio una excepcion en get_slice')
            response = self.make_response(INTERNAL_ERROR)
        finally:
            self.socket.sendall(response)

    def quit(self):
        response = self.make_response(CODE_OK)
        self.socket.send(response)
        self.socket.close()
        self.is_connected = False

    def exit(self):
        self.socket.close()
        self.is_connected = False

    def make_response(self, code, msg=""):
        return str(code).encode() + b' ' + error_messages[code] + EOL + msg
