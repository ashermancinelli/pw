#!/usr/bin/env python3

import os
import socket
import click
import threading

def handle_conn(chunk_size, secret, package):
    def handler(conn, addr):
        print('Accepted from ', addr)
        try:
            got = conn.recv(chunk_size).decode().strip()
            print(got)

            if not got:
                conn.sendall(b'Must send secret as first message.\n')
                raise Exception()

            if got != secret:
                conn.sendall(b'Recieved packet did not match secret.\n')
                raise Exception()

            conn.sendall(package.encode())

        finally:
            conn.close()

    return handler


@click.command()
@click.option('--port', default=5555)
@click.option('--host', default='localhost', help='Use `public` for public host')
def main(port, host):

    assert os.path.exists('secret') and os.path.exists('package'), \
            "Must have file secret and package present in cwd"

    if host == 'public':
        host = socket.gethostname()

    secret = open('secret', 'r').read().strip()
    package = open('package', 'r').read().strip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        t = threading.Thread(
                target=handle_conn(256, secret, package),
                args=(conn, addr),
                daemon=True)
        t.run()

if __name__ == '__main__':
    main()
