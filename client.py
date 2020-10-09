#!/usr/bin/env python3

import os
import socket
import click

@click.command()
@click.argument('secret', nargs=1)
@click.option('--port', default=5555)
@click.option('--host', default='localhost')
def main(secret, port, host):

    if host == 'public':
        host = socket.gethostname()

    secret = open('secret', 'r').read().strip()
    package = open('package', 'r').read().strip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(secret.encode())
    ans = sock.recv(256).strip()
    print(ans.decode())

if __name__ == '__main__':
    main()
