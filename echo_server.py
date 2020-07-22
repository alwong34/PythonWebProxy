#!/usr/bin/env python3

import argparse
import json
# add additional import statements here
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def get_simple_response(message):
    return message

def get_hello_response(message):
    return "Hello, " + message

def get_request_response(message):
    # TODO: Parse request line of standard HTTP request
    request = { 'method': 'GET', 'path': '/index.html', 'version': 'HTTP/1.1'}
    return json.dumps(request) # converts dictionary to JSON string

def get_header_response(message):
    # TODO: Parse header line of standard HTTP request
    header = { 'name': 'Host', 'value': message }
    return json.dumps(header) # converts dictionary to JSON string

def main():
    # more argument parsing examples at https://realpython.com/command-line-interfaces-python-argparse/

    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port of Echo Server', default=9999)
    parser.add_argument('-m', '--mode', choices=['simple', 'hello', 'request', 'header'], default='simple')
    parser.add_argument('text', type=str, help='UTF-8 text to send to echo server')

    # parse the command line
    args = parser.parse_args()

    # examine the input
    print(args.port)
    print(args.text)
    print(args.text.encode('utf-8'))
    print(args.text.encode('utf-8').hex())
    print(args.mode)


    # SET UP SERVER SOCKET
    # Use sockopt to avoid bind() exception: OSError: [Errno 48] Address already in use
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, args.port))
        s.listen()
        # ACCEPT NEW CONNECTIONS (in a loop / one at a time)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
    
            # RECEIVE BYTES AND DECODE AS STRING
                message = data.decode('utf-8')

                if args.mode == 'simple':
                    response = get_simple_response(message)
                elif args.mode == 'hello':
                    response = get_hello_response(message)
                elif args.mode == 'request':
                    response = get_request_response(message)
                elif args.mode == 'header':
                    response = get_header_response(message)

                print(response)
                conn.sendall(response.encode('utf-8'))
    # ENCODE STRING TO BYTES USING UTF-8 AND SEND RESPONSE TO CLIENT

    # CLOSE CONNECTION TO CLIENT BUT KEEP SERVER SOCKET OPEN

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()