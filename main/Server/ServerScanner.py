import errno
import socket
import threading
from queue import Queue

import netifaces

TIMEOUT = 2
SERVER_ADD = 'add'
SERVER_REMOVE = 'remove'
SERVER_TEST_REMOVE = "test-remove"


class ServerScanner(threading.Thread):
    """
    A scanner of servers
    """

    def __init__(self, port_min=3000, port_max=3020, max_thread=100,
                 list_update_function=lambda add_remove, host_port: None):
        """
        Constructor
        """
        super().__init__()

        self.setDaemon(True)

        self.server_detected_list = []
        self.stop_scan = False

        self.list_update_function = list_update_function

        self.port_min = port_min
        self.port_max = port_max

        socket.setdefaulttimeout(TIMEOUT)

        self.max_thread = max_thread
        self.thread_running = 0
        self.threads = Queue()

        self.list_in_queue = []

    # noinspection SpellCheckingInspection
    def run(self):
        """
        Start the scan
        :return: None
        """
        while not self.stop_scan:
            # verify if server not close
            if SERVER_TEST_REMOVE not in self.list_in_queue and len(self.server_detected_list) >= 1:
                thread = threading.Thread(target=self.verify_detected_server)
                self.threads.put(thread)
                self.list_in_queue.append(SERVER_TEST_REMOVE)

            interface_list = netifaces.interfaces()

            for interface in interface_list:
                if self.stop_scan:
                    break

                try:
                    mask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
                    ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']

                    if ip != "127.0.0.1":  # Don't scan the local loop
                        # Scan all ip

                        current_ip, ip_max = self.get_min_max_ip(ip, mask)

                        while current_ip != ip_max and current_ip != '255.255.255.255':
                            if self.stop_scan:
                                break

                            if current_ip not in self.list_in_queue:
                                thread = threading.Thread(target=self.scan_ip, kwargs={'ip': current_ip})
                                thread.setDaemon(True)
                                self.threads.put(thread)
                                self.update_thread()
                                self.list_in_queue.append(current_ip)

                            current_ip = self.increment_ip(current_ip)

                        if self.stop_scan:
                            break

                        if current_ip not in self.list_in_queue:
                            thread = threading.Thread(target=self.scan_ip, kwargs={'ip': current_ip})
                            thread.setDaemon(True)
                            self.threads.put(thread)
                            self.update_thread()
                            self.list_in_queue.append(current_ip)

                except KeyError:
                    continue  # if AF_INET don't exist

    def update_thread(self):
        """
        Start if possible threads
        :return: None
        """
        if not self.threads.empty() and self.thread_running < self.max_thread:
            self.threads.get_nowait().start()
            self.thread_running += 1

    def scan_ip(self, ip):
        """
        Scan the ip
        :param ip: the ip to scan
        :return: None
        """
        try:
            for p in range(self.port_min, self.port_max + 1):
                if self.stop_scan:
                    return None

                # if ip == '192.168.1.123':
                #     print(p)

                if (ip, p) not in self.server_detected_list and self.test_address(ip, p):
                    self.add_server_detected(ip, p)

        except socket.gaierror:
            pass

        self.thread_running -= 1
        self.update_thread()
        self.list_in_queue.remove(ip)

    def add_server_detected(self, host, port):
        """
        When a server is detected
        :param host: the host detected
        :param port: the port detected
        :return: None
        """
        if (host, port) not in self.server_detected_list:
            # print("{} - Port {} is open".format(host, port))
            self.server_detected_list.append((host, port))
            self.list_update_function(SERVER_ADD, (host, port))

    def remove_server_detected(self, host, port):
        """
        When a server is quit
        :param host: The host
        :param port: The port
        :return: None
        """
        if (host, port) in self.server_detected_list:
            # print("{} - Port {} is close".format(host, port))
            self.server_detected_list.remove((host, port))
            self.list_update_function(SERVER_REMOVE, (host, port))

    def verify_detected_server(self):
        """
        verify that server is up
        :return: None
        """
        for ip, port in self.server_detected_list[:]:
            try:
                if not self.test_address(ip, port):
                    self.remove_server_detected(ip, port)
            except socket.gaierror:
                self.remove_server_detected(ip, port)

        self.list_in_queue.remove(SERVER_TEST_REMOVE)
        self.thread_running -= 1
        self.update_thread()

    @staticmethod
    def test_address(host, port):
        """
        Test an address
        :param host: the ip to test
        :param port: the port to test
        :return: if the port is open
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        result = s.connect_ex((host, port))
        s.close()
        if result == errno.EHOSTDOWN or result == errno.EHOSTUNREACH or result == errno.EWOULDBLOCK or \
                result == errno.ECONNABORTED:
            raise socket.gaierror
        return result == 0

    @staticmethod
    def get_min_max_ip(ip, mask):
        """
        Get the minimum and the maximum ip of a mask
        :param ip: An ip of the mask
        :param mask: The mask to scan
        :return: (Minimum IP, Maximum IP)
        """
        try:
            ip_numbers_list = [int(n) for n in ip.split('.')]
        except ValueError:
            return None
        ip_numbers_binary_list = ["{:0>8b}".format(n) for n in ip_numbers_list]

        try:
            mask_numbers_list = [int(n) for n in mask.split('.')]
        except ValueError:
            return None
        mask_numbers_binary_list = ["{:0>8b}".format(n) for n in mask_numbers_list]

        minimum_ip_binary = []
        maximum_ip_binary = []

        for number in range(0, 4):
            minimum_ip_binary.append('')
            maximum_ip_binary.append('')
            for index_octet in range(0, 8):
                if mask_numbers_binary_list[number][index_octet] == '1':
                    minimum_ip_binary[number] += ip_numbers_binary_list[number][index_octet]
                    maximum_ip_binary[number] += ip_numbers_binary_list[number][index_octet]

                else:
                    minimum_ip_binary[number] += '0'
                    maximum_ip_binary[number] += '1'

        minimum_ip = '.'.join([str(int(n, base=2)) for n in minimum_ip_binary])
        maximum_ip = '.'.join([str(int(n, base=2)) for n in maximum_ip_binary])

        return minimum_ip, maximum_ip

    @staticmethod
    def increment_ip(ip):
        """
        Increment an ip
        :param ip: the ip to increment
        :return: The final ip
        """
        try:
            ip_numbers_list = [int(n) for n in ip.split('.')]
        except ValueError:
            return None

        ip_numbers_list[3] += 1
        if ip_numbers_list[3] >= 256:
            ip_numbers_list[3] = 0

            ip_numbers_list[2] += 1
            if ip_numbers_list[2] >= 256:
                ip_numbers_list[2] = 0

                ip_numbers_list[1] += 1
                if ip_numbers_list[1] >= 256:
                    ip_numbers_list[1] = 0

                    ip_numbers_list[0] += 1
                    if ip_numbers_list[0] >= 256:
                        raise RuntimeError("Can't increment, the ip is 255.255.255.255")

        return '.'.join([str(n) for n in ip_numbers_list])
