#!/user/bin/env python
import sys
import socket
import logging
import select


class UdpPingerServer(object):

    def __init__(self, port=9999):
        self._socket = socket.socket(socket.AF_INET,
                                     socket.SOCK_DGRAM)
        self._server_address = ('', port)
        self._socket.bind(self._server_address)
        self._socket.setblocking(0)

    def start_server(self):
        logging.info('UDP Ping Server running at 0.0.0.0:%s',
                     self._server_address[1])
        while True:
            r = select.select([self._socket.fileno()], [], [], 1)[0]
            if self._socket.fileno() in r:
                data, addr = self._socket.recvfrom(1024)
                logging.info('Recieve Ping from %s:%s', addr[0], addr[1])
                self._socket.sendto(data, addr)


if __name__ == '__main__':
    logging.basicConfig(
        filename='server_log.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    if len(sys.argv) == 2:
        port = 9999
        try:
            port = int(sys.argv[1])
        except:
            logging.error('Invalid port')
            exit(1)
        server = UdpPingerServer(port)
        server.start_server()
    else:
        print 'Usage: python server.py <port>'
        exit(1)
