#!/usr/bin/env python3

# add import statements here
import argparse
import socket
import json
from urllib.parse import urlparse
from enum import Enum, auto
from datetime import datetime
# define classes, enums, etc here
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class MessageType(Enum):
    REQUEST = auto() # constant values are auto-assigned
    RESPONSE = auto() # constant values are auto-assigned

# define functions here
def parse_message(buffer, message_type):
    # Parse a buffer of bytes and return: 
    try:
        # initialize an empty dictionary
        message = {}

        # get the first line of buffer
        line, unparsed_buff = parse_line(buffer)

        message['type'] = message_type
        if message['type'] is MessageType.REQUEST:
            # parse request fields ...
            # split the first line of HTTP request
            fields = line.split(' ', 2)
            message['method'] = fields[0]# HTTP method name such as GET
            message['uri'] = fields[1] # address or resource name from the request, such as www.uw.edu
            message['version'] = fields[2]# HTTP version such as HTTP/1.0
        elif message['type'] is MessageType.RESPONSE:
            # parse response fields...
            fields = line.split(' ', 2)
            message['version'] = fields[0]
            message['code'] = fields[1]
            message['text'] = fields[2]

        # get headers from rest of buffer
        headers = []
        line, unparsed_buff = parse_line(unparsed_buff)
        while line != '':
            if line is None:
                raise Exception
                
            header_pair = line.partition(':')
            new_header = {'name': header_pair[0].strip(), 'value': header_pair[2].strip()}
           
            if new_header['name'] == 'Content-Length':
                message['content-length'] = int(new_header['value'])
            line, unparsed_buff = parse_line(unparsed_buff)
            if line[:1] == " ": 
                new_header['value'] += " " + line.strip()
                line, unparsed_buff = parse_line(unparsed_buff)

            headers.append(new_header)

        # parse bytes and assign key / value pairs such as ...
        message['headers'] = headers # List of headers

        if 'content-length' in message.keys():
            if message['content-length'] > 0:
                if len(unparsed_buff) < message['content-length']:
                    return None, buffer
                message['payload'] = unparsed_buff[0:message['content-length']]
                unparsed_buff = unparsed_buff[message['content-length']:len(unparsed_buff)]

        # If parsing is successful, return a completed message (if applicable) and unused bytes
        return message, unparsed_buff
    except:
        # If parsing fails, return the entire buffer and an indicator that parsing was incomplete
        return None, buffer
    
def parse_line(data):
    fields = data.partition(b'\n')

    if len(fields[1]) == 0:
        return None, data

    line = fields[0].rstrip(b'\r')
    line = line.decode('iso-8859-1')

    if len(fields[2]) == 0:
        return line, None

    return line, fields[2]

# returns the host and port
# run by doing:  h, p = parse_uri(dest)
def parse_uri(uri):
    uri_parts = urlparse(uri)
    scheme = uri_parts.scheme
    host = uri_parts.hostname
    # urlparse can't deal with partial URI's that don't include the 
    # protocol, e.g., push.services.mozilla.com:443
    if host: # correctly parsed
        if uri_parts.port:
            port = uri_parts.port
        else:
            port = socket.getservbyname(scheme)
    else: # incorrectly parsed
        uri_parts = uri.split(':')
        host = uri_parts[0]
        if len(uri) > 1:
            port = int(uri_parts[1])
        else:
            port = 80
    return host, port

def build_message(message):
    result = ""

    if message['type'] is MessageType.REQUEST:
        message_header = '{} {} {}\r\n'.format(message['method'], message['uri'], 'HTTP/1.0')
    elif message['type'] is MessageType.RESPONSE:
        message_header = '{} {} {}\r\n'.format(message['version'], message['code'], message['text'])
    
    result = result + message_header

    for header in message['headers']:
        result = result + '{}\r\n'.format(header['name'] + ": " + header['value']) # Format each header properly

    # Don't forget to add a terminating CRLF
    result = result + '\r\n'
    # Encode the header portion of the message as bytes
    result = result.encode('iso-8859-1')
    # Do you have a message body? Add it back now
    if 'payload' in message.keys():
        result = result + message['payload']
    return result

def main():
    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port for HTTP proxy', default=9999)

    # parse the command line
    args = parser.parse_args()

    # SET UP SERVER SOCKET
    # Use sockopt to avoid bind() exception: OSError: [Errno 48] Address already in use
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, args.port))
        s.listen()
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        while True:
            # ACCEPT NEW CONNECTIONS (in a loop / one at a time)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)

                # Declare an empty buffer
                buffer = b''

                while True:
                    data = conn.recv(1024)
                    if data is None:
                        break

                    if not data:
                        break
                    # add new data to the buffer
                    buffer = buffer + data

                    # parse the message
                    message, buffer =  parse_message(buffer, MessageType.REQUEST)
                    if message is not None:
                        break
                
                # LOGGING / OUTPUT
                # header_names = [h['name'] for h in message['headers']]
                # out = ', '.join(header_names)
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("[%d/%b/%Y:%H:%M:%S %f]") 
                
                referer_header = "-"
                for header in message['headers']:
                    if header['name'] == "Referer":
                        referer_header = "\"" + header['value'] + "\""

                user_agent_header = "-"
                for header in message['headers']:
                    if header['name'] == "User-Agent":
                        user_agent_header = "\"" + header['value'] + "\""

                content_length = 0
                if 'content-length' in message.keys():
                    content_length = message['content-length']
                # print('Timestamp: ' + timestampStr)
                # print('User-Agent Header ' + user_agent_header)
                # print('Referer Header: ' + referer_header + '\n')
                # print('Connection Source: ', addr)
                # print('HTTP Method: ' + message['method'])
                # print('Destination: ' + message['uri'])
                # print('Headers: ' + out)
                # if 'content-length' in message.keys():
                #     print('Content-Length: ' + str(message['content-length']))
                # if 'payload' in message.keys():
                #     print('Payload: ' + str(message['payload']))

                # print(addr + ' ' + timestampStr + "\"" + message['method'] + " " +  )
                # PROXY REQUEST
                dhost, dport = parse_uri(message['uri'])
                data = build_message(message)
                # print('\n')
                # print('dhost: ' + str(dhost) + ' dport: ' + str(dport))
                # print('\n')

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn_out:
                    conn_out.connect((dhost, dport))
                    conn_out.sendall(data)
                    outbound_buffer = b''

                    while True:
                        data = conn_out.recv(4096)
                        if data is None:
                            break
                        if not data:
                            break
                        outbound_buffer = outbound_buffer + data
                        response, outbound_buffer = parse_message(outbound_buffer, MessageType.RESPONSE)
                        if response is not None:
                            break
                    
                    # response_header_names = [h['name'] for h in response['headers']]
                    # response_out = ', '.join(response_header_names)
                    # print('Protocol Version: ' + response['version'])
                    # print('Status Code: ' + response['code'])
                    # print('Text Reason: ' + response['text'])
                    # print('Headers: ' + response_out)
                    # if 'content-length' in response.keys():
                    #     print('Content-Length: ' + str(response['content-length']))
                    # if 'payload' in response.keys():
                    #     print('Payload: ' + str(response['payload']))

                    format_log = '{} {} \"{} {} {}\" {} {} {} {}'.format(host_ip, timestampStr, message['method'], message['uri'], message['version'],
                       response['code'], content_length, referer_header, user_agent_header)
                    # print(message['headers'])
                    print(format_log)

                    data = build_message(response)
                    conn.sendall(data)
                    conn.close()

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()