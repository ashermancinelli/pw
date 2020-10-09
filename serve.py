#!/usr/bin/env python3

import os
import socket
import socketserver
import click
import threading

def pwserver(secret, package):
    class PWServer(socketserver.StreamRequestHandler):
        def handle(self):
            self.data = self.rfile.readline().strip().decode()
            if self.data != secret:
                print('Failure')
                self.wfile.write('Incorrect password.\n'.encode())
            else:
                print('Success')
            self.wfile.write(package.encode() + b'\n')
    return PWServer


@click.command()
@click.option('--port', default=5555)
@click.option('--host', default='localhost', help='Use `public` for public host')
def main(port, host):

    assert os.path.exists('secret') and os.path.exists('package'), \
            "Must have file secret and package present in cwd"

    if host == 'public':
        host = ''

    secret = open('secret', 'r').read().strip()
    package = open('package', 'r').read().strip()

    print('Serving on', host, port)
    server = socketserver.TCPServer((host, port), pwserver(secret, package))
    server.serve_forever()


if __name__ == '__main__':
    main()
