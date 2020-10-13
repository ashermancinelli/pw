#!/usr/bin/env python3

import os
import socket
import click
from cryptography.fernet import Fernet
import json

@click.command()
@click.option('--port', default=5555)
@click.option('--host', default='localhost')
@click.option('--secret-file', default='secret')
@click.option('--query', default=None)
def main(port, host, secret_file, query):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    secret = open(secret_file, 'rb').read()
    sock.sendall(secret + b'\n')
    f = Fernet(secret)

    ans = b''
    while True:
        resp = sock.recv(1)
        if resp == b'':
            break
        ans += resp

    package = f.decrypt(ans).decode()
    j = json.loads(package)
    ret = dict()
    if query is None:
        ret = j
    else:
        for k, v in j.items():
            if query in k:
                ret[k] = v

    print(json.dumps(ret, indent=2))

if __name__ == '__main__':
    main()
