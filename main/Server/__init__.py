import queue
import select
import socket
import threading
import time


TIMEOUT = 0.01
ENCODING = "UTF-8"
MESSAGE_SEPARATOR = '\x00'


class Server(threading.Thread):
    """
    A serve class
    """

    def __init__(self, ip=None, port=12345, max_clients_connected=5, on_message_function=lambda message: None,
                 on_client_connect_function=lambda client: None, on_client_disconnect_function=lambda client: None):
        """
        Constructor
        :param ip: the ip of the server
        :param port: the port of the server
        """
        super().__init__()

        self.setName("Server")

        if ip is None:
            self.ip = self.get_ip()
        else:
            self.ip = ip
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_is_on = False
        self.accept = False

        self.max_clients_connected = max_clients_connected

        self.socket.setblocking(True)

        self.input_list = [self.socket]
        self.output_list = []

        self.on_message_function = on_message_function
        self.on_client_connect_function = on_client_connect_function
        self.on_client_disconnect_function = on_client_disconnect_function

        self.message_queues = {}

    def start_server(self):
        """
        Start the server
        :return: If is do
        """
        if not self.server_is_on:
            try:
                self.socket.bind((self.ip, self.port))
                self.log("Start the server", "Server")
                self.server_is_on = True
                self.start()
                return True
            except socket.error as e:
                self.error("Can't start the server. Error n°" + str(e.errno) + " (" + e.strerror + ")", "Server")
        return False

    def run(self):
        """
        Run the accept loop
        :return: None
        """
        self.socket.listen(self.max_clients_connected)
        while self.server_is_on:
            try:
                readable, writable, exceptional = select.select(self.input_list, self.output_list, self.input_list,
                                                                TIMEOUT)
            except (socket.error, ValueError):
                # When the server is close
                break
            for s in readable:

                if s is self.socket:
                    try:
                        client_socket, address = self.socket.accept()
                        self.try_connect(client_socket)
                    except OSError:
                        break
                else:
                    message = s.recv(2048)
                    if message:
                        self.on_message_function(message)
                    else:
                        self.disconnect(s)
                        break

            for s in writable:
                try:
                    message = self.message_queues[s].get_nowait()
                except queue.Empty:
                    self.output_list.remove(s)
                else:
                    s.send(message)

            for s in exceptional:
                self.warn("The client-{} ad an error !".format(*s.getpeername()), "Server")
                self.disconnect(s)

        self.kick_all()

    def kick_all(self):
        """
        Kick all client
        :return: None
        """
        index = 0  # the start of the list
        while len(self.input_list) >= index + 1:
            if self.input_list[index] is self.socket:
                index += 1
            else:
                self.disconnect(self.input_list[index])

    def stop_server(self):
        """
        Stop the server
        :return: If is do
        """
        if self.server_is_on:
            self.kick_all()
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
                self.log("Server stopped", "Server")
                self.server_is_on = False
                return True
            except socket.error:
                pass
        return False

    def try_connect(self, client_socket):
        """
        Try to connect the client to the server
        :param client_socket: The socket of the client
        :return: None
        """
        self.input_list.append(client_socket)
        self.message_queues[client_socket] = queue.Queue()

        self.log("Client-{}:{} is connected".format(*client_socket.getpeername()), "Server")

        self.on_client_connect_function(client_socket)

    def disconnect(self, client_socket):
        """
        Disconnect the client
        :param client_socket: The client
        :return: None
        """
        peer_name = client_socket.getpeername()
        self.input_list.remove(client_socket)
        if client_socket in self.output_list:
            self.output_list.remove(client_socket)

        client_socket.close()

        self.on_client_disconnect_function(client_socket)

        self.log("Client-{}:{} is disconnected".format(*peer_name), "Server")

        del self.message_queues[client_socket]

    def send_message_to_all(self, message):
        """
        Send a message to all client
        :param message: the message to send ! In binary !
        :return: None
        """
        for s in self.input_list:
            if s is not self.socket:
                self.send_message(s, message)

    def send_message(self, client, message):
        """
        Send a message to a client
        :param client: the client
        :param message: the message ! In binary !
        :return: None
        """
        if client in self.input_list and client is not self.socket:
            self.output_list.append(client)
            self.message_queues[client].put(message)

    @staticmethod
    def log(msg, thread_name=threading.current_thread().getName()):
        """
        Print a message
        :param msg: the message
        :param thread_name: the name of the thread
        :return: None
        """
        print("[Log / " + thread_name + " / " + Server.get_time() + "]: " + msg)

    @staticmethod
    def warn(msg, thread_name=threading.current_thread().getName()):
        """
        Print a message
        :param msg: the message
        :param thread_name: the name of the thread
        :return: None
        """
        print("[Warn / " + thread_name + " / " + Server.get_time() + "]: " + msg)

    @staticmethod
    def error(msg, thread_name=threading.current_thread().getName()):
        """
        Print a message
        :param msg: the message
        :param thread_name: the name of the thread
        :return: None
        """
        print("[ERROR / " + thread_name + " / " + Server.get_time() + "]: " + msg)

    @staticmethod
    def get_time():
        """
        Return current date and time
        :return: a string which is the current time
        """
        return time.strftime("%D %X")

    @staticmethod
    def get_ip():
        """
        Get the current ip
        :return: The ip
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except socket.error:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    @staticmethod
    def exist(ip, port):
        """
        Get if a connexion is possible
        :param ip: The ip to connect
        :param port: The port to connect
        :return: Boolean if is possible
        """
        can_connect = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = s.connect_ex((ip, port))

            if result == 0:
                can_connect = True
        except socket.error:
            pass
        finally:
            s.close()

        return can_connect

    @staticmethod
    def encode_message(message):
        """
        Encode the message
        :param message: The message  ! must be a string !
        :return: The message in binary
        """
        message += MESSAGE_SEPARATOR
        return message.encode(ENCODING)

    @staticmethod
    def decode_message(message):
        """
        Decode the message
        :param message: The message  ! must be bytes !
        :return: A list of messages
        """
        message = message.decode(ENCODING)
        message = message.split(MESSAGE_SEPARATOR)
        return message[:-1]
