#!/user/bin/env python
import sys
import socket
import logging
import time


class UdpPingerClient(object):
    MESSAGE = 'UDP PING'
    COUNT = 4
    SIZE = 1024
    TIMEOUT = 2.0

    def __init__(self, host, port):
        addr = socket.gethostbyname(host)
        self._server_address = (addr, port)
        self._server_name = socket.gethostbyaddr(addr)[0]
        self._socket = socket.socket(socket.AF_INET,
                                     socket.SOCK_DGRAM)
        self._socket.settimeout(UdpPingerClient.TIMEOUT)

    def start_client(self):
        logging.info('UDP Ping Client started!')
        for i in range(UdpPingerClient.COUNT):
            try:
                self._socket.sendto(UdpPingerClient.MESSAGE,
                                    self._server_address)
                data = self._socket.recv(UdpPingerClient.SIZE)
                logging.info('%s byte from %s:%s',
                             len(data),
                             self._server_address[0],
                             self._server_address[1])
                if i != UdpPingerClient.COUNT - 1:
                    time.sleep(1)
            except socket.timeout:
                logging.error('Timeout')


if __name__ == '__main__':
    logging.basicConfig(
        filename='client_log.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    if len(sys.argv) == 3:
        try:
            addr = sys.argv[1]
            port = int(sys.argv[2])
        except:
            logging.error('Invalid port or ip address/host')
            exit(1)
    if len(sys.argv) == 2:
        try:
            addr_port = sys.argv[1].split(':')
            addr = addr_port[0]
            port = int(addr_port[1])
        except:
            logging.error('Invalid port or ip address/host')
            exit(1)
        client = UdpPingerClient(addr, port)
        client.start_client()
    else:
        print 'Usage: python client.py <ip> <port> | <ip:port>'
        exit(1)
