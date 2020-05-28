import queue
import select
import socket
import threading
import time

from main import Server


class Client(threading.Thread):
    """
    A client for socket server
    """

    def __init__(self, ip, port=12345, on_message_function=lambda message: None,
                 on_connection_function=lambda: None, on_disconnection_function=lambda: None):
        """
        Constructor
        :param ip: The ip of the host
        :param port: THe port of the host
        :param on_message_function: A function when the client receive a message
        """
        super().__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ip = ip
        self.port = port

        self.connected = False

        self.on_message_function = on_message_function
        self.on_connection_function = on_connection_function
        self.on_disconnection_function = on_disconnection_function

        self.message_queue = queue.Queue()

    def connect(self):
        """
        Connect to the server
        :return: If is do
        """
        if not self.connected:
            try:
                self.socket.connect((self.ip, self.port))
                self.log("Connected with the server", "Client")
                self.connected = True
                self.start()

                self.on_connection_function()
                return True
            except socket.error as e:
                self.error("Can't connect to the server. Error n°" + str(e.errno) + " (" + e.strerror + ")",
                           "Client")

        return False

    def close_connection(self):
        """
        Close the connection
        :return: None
        """
        if self.connected:
            try:
                self.socket.close()
                self.log("The connection with the server is close", "Client")
                self.on_disconnection_function()
            except socket.error as e:
                self.error("Can't close the connexion. Error n°" + str(e.errno) + " (" + e.strerror + ")",
                           "Client")
            else:
                self.connected = False

    def run(self):
        """
        When the thread is
        :return:
        """
        while self.connected:
            output_list = []
            if not self.message_queue.empty():
                output_list = [self.socket]

            try:
                readable, writable, exceptional = select.select([self.socket], output_list, [self.socket],
                                                                Server.TIMEOUT)
            except (ValueError, OSError):
                self.close_connection()
                break

            if readable:
                message = self.socket.recv(2048)
                if message:
                    messages = Server.Server.decode_message(message)
                    for msg in messages:
                        try:
                            self.on_message_function(msg)
                        except Exception as e:
                            self.error("Error: " + str(e), "Client")
                else:
                    self.close_connection()
                    break

            if writable:
                self.socket.send(self.message_queue.get_nowait())

            if exceptional:
                self.close_connection()

    def send_message(self, message):
        """
        Send a message to the server
        :param message: The message to send  ! In binary !
        :return: None
        """
        self.message_queue.put(message)

    @staticmethod
    def log(msg, thread_name=threading.current_thread().getName()):
        """
        Print a message
        :param msg: the message
        :param thread_name: the name of the thread
        :return: None
        """
        print("[Log / " + thread_name + " / " + Client.get_time() + "]: " + msg)

    @staticmethod
    def warn(msg, thread_name=threading.current_thread().getName()):
        """
        Print a message
        :param msg: the message
        :param thread_name: the name of the thread
        :return: None
        """
        print("[Warn / " + thread_name + " / " + Client.get_time() + "]: " + msg)

    @staticmethod
    def error(msg, thread_name=threading.current_thread().getName()):
        """
        Print a message
        :param msg: the message
        :param thread_name: the name of the thread
        :return: None
        """
        print("[ERROR / " + thread_name + " / " + Client.get_time() + "]: " + msg)

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
