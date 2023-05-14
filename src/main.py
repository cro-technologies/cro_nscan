import os
import argparse
import socket
import threading
import random
from concurrent.futures import ThreadPoolExecutor


class OPort:
    def __init__(self):
        self.open_ports = []

    def print_info_from_ip(self, host, port):
        family, type, proto, sockaddr, canonname = socket.getaddrinfo(host, port)[
            0]
        print(f"{family}\t{type}\t{proto}\t{sockaddr}\t\t{canonname}")

    def scan(self, host, port):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.settimeout(float(random.randint(1, 5)))
            self.soc.connect((host, port))
            # print('Open port %d' % port)
            self.print_info_from_ip(host, port)
        except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError, OSError)as e:
            pass
        except KeyboardInterrupt:
            exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('-tc', '--thread_count', type=int,
                        default=min(32, (os.cpu_count()+1)+4), help="Number of threads to execute per scan. Default is base on your machine thread count")
    parser.add_argument('-p', '--port', type=str,
                        help="Example: from (100-200) or a specific port 1000", default="10-65535")
    args = parser.parse_args()

    host = args.host
    ports = args.port.split('-')

    mp: int = 65535

    o = OPort()

    if (len(ports) > 1):
        if (int(ports[0]) > mp or int(ports[1]) > mp):
            print('Invalid port range')
            exit(1)
        print("\nfamily\ttype\tproto\tsockaddr\tcanonname\n")
        with ThreadPoolExecutor(args.thread_count) as executor:
            for port in range(int(ports[0]), int(ports[1])+1):
                executor.submit(o.scan, host, int(port))
    else:
        if (int(ports[0]) > mp):
            print('Invalid port range')
            exit(1)
        o.scan(host, int(ports[0]))
