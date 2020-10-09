#!/usr/bin/env python3

import os
import socket
import click

@click.command()
@click.argument('secret', nargs=1)
@click.option('--port', default=5555)
@click.option('--host', default='localhost')
def main(secret, port, host):

    secret = open('secret', 'r').read().strip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connect')
    sock.connect((host, port))
    print('connect')
    sock.sendall(secret.encode())
    print('connect')
    ans = ''
    while True:
        ans = sock.recv(16).strip()
        if '\n' in ans:
            break
    print(ans.decode())

if __name__ == '__main__':
    main()
