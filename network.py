import socket
import selectors

class ClientManager():
    def __init__(self, addr=''):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)

        if not addr:
            addr = ('0.0.0.0', 7777)
            print('listening on', addr)
            self.socket.bind(addr)
            self.socket.listen(32)
            self.selector = selectors.DefaultSelector()
            self.selector.register(self.socket, selectors.EVENT_READ)
        else:
            print('connecting to', addr)
            try:
                self.socket.connect((addr, 7777))
            except BlockingIOError:
                pass 

    def _accept_wrapper(self, sock):
        client_socket, client_address = sock.accept()
        print('connection from', client_address)
        client_socket.setblocking(False)
        self.selector.register(client_socket, selectors.EVENT_READ, data=client_address)

    def _close_wrapper(self, client_socket):
        self.selector.unregister(client_socket)
        client_socket.close()
    
    def _handle_client(self, client_socket, message):
        try:
            client_socket.sendall(message)
        except Exception as e:
            print('error occurred:', e) 
    
    def send(self, msg):
        while len((events := self.selector.select(timeout=0))):
            for selector_key, _ in events:
                if selector_key.fileobj == self.socket:
                    self._accept_wrapper(selector_key.fileobj)
                else:
                    self._close_wrapper(selector_key.fileobj)

        for _, selector_key in self.selector.get_map().items():
            if selector_key.data is not None:
                client_socket = selector_key.fileobj
                self._handle_client(client_socket, msg)
    
    def recv(self):
        try:
            data = self.socket.recv(1024)
        except BlockingIOError:
            return None
        else:
            return data


