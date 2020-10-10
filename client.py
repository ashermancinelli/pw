#!/usr/bin/env python3

import os
import socket
import click

@click.command()
@click.argument('secret', nargs=1)
@click.option('--port', default=5555)
@click.option('--host', default='localhost')
def main(secret, port, host):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(secret.encode() + b'\n')
    ans = ''
    while True:
        resp = sock.recv(1)
        if resp == b'':
            break
        ans += resp.decode()
    print(ans.strip())

if __name__ == '__main__':
    main()
