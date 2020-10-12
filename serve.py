#!/usr/bin/env python3

import os
import socket
import socketserver
import click
import threading
from cryptography.fernet import Fernet

def pwserver(secret: bytes, package: bytes):
    class PWServer(socketserver.StreamRequestHandler):
        def handle(self):
            self.data = self.rfile.readline().strip()
            if self.data != secret:
                print('Failure')
                self.wfile.write('Incorrect password.\n'.encode())
                raise Exception()
            else:
                print('Success')
            self.wfile.write(package + b'\n')
    return PWServer


@click.command()
@click.option('--port', default=5555)
@click.option('--host', default='localhost', help='Use `public` for public host')
@click.option('--secret-file', default='secret')
@click.option('--package-file', default='package')
def main(port, host, secret_file, package_file):

    assert os.path.exists(secret_file) and os.path.exists(package_file), \
            "Must have file secret and package present in cwd"

    secret: str = open(secret_file, 'rb').read().strip()
    package: str = open(package_file, 'r').read().strip()
    f = Fernet(secret)
    package: bytes = f.encrypt(package.encode())

    print('Serving on', host, port)
    server = socketserver.TCPServer(
            (host if host != 'public' else '', port),
            pwserver(secret, package))
    server.serve_forever()


if __name__ == '__main__':
    main()
