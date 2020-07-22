#!/usr/bin/env python3

import argparse
# add additional import statements here
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def main():
    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port of Echo Server', default=9999)
    parser.add_argument('text', type=str, help='UTF-8 text to send to echo server')

    # parse the command line
    args = parser.parse_args()
    message = args.text

    # ESTABLISH SOCKET AND CLIENT CONNECTION
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, args.port))
        # SEND MESSAGE
        s.sendall(message.encode('utf-8'))
        # RECEIVE RESPONSE
        response = s.recv(1024).decode()
        # EXAMINE RESPONSE
        print('INPUT: {}'.format(message))
        print('RESPONSE: {}'.format(response))
        print('UTF-8 ENCODING: {}'.format(response.encode("utf-8"))) # Encode response as UTF-8
# if statement so main() runs by default from command line
if __name__=="__main__":
    main()