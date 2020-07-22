# Lab 6 Report - Python and Socket Basics

INFO 314 
DATE: 5/12/2020
NAME: Alex Wong

## Overview  

**In the remaining weeks of the quarter, we will create a network service using the Python sockets API. In this lab, we will introduce the basic concepts of network programming with a Sockets API and build a pair of toy applications.**

**Follow the procedures provided to you on Canvas and the course website. When you are finished, answer the following questions and include the completed report in your Pull Request. Be sure to cite any external references that you use.**

## Questions

1. **What two values are returned by the accept() function in the Python socket library?**

   The accept() function returns a new socket object representing the connection and a tuple holding the address of the client.

2. **Briefly describe the difference between bind(), listen(), and accept()?**

   bind() - used to associate the socket with a specific network interface and port number

   listen() - enables a server to accept() connections and specified the number of unaccepted connections the system will allow before refusing new connections

   accept() - used to accept, or complete the connection

3. **How can we get a server socket to listen and accept connections on all available IPv4 interfaces and addresses?**

   If you pass an empty string as the host to the bind() function a server socket will listen and accept connections on all available IPv4 interfaces.

4. **How do we create a server socket that restricts communication to processes running on the same host?**

   To create a server socket that restricts communication to processes running on the same host you can pass the 127.0.0.1 address which is the loopback interface to bind()

5. **What happens if a client or server calls recv() on a connection, but there isn't any data waiting to be processed?**

   if a [`recv()`](https://docs.python.org/2/library/socket.html#socket.socket.recv) call doesn’t find any data, or if a [`send()`](https://docs.python.org/2/library/socket.html#socket.socket.send) call can’t immediately dispose of the data, an [`error`](https://docs.python.org/2/library/socket.html#socket.error) exception is raised

   https://docs.python.org/2/library/socket.html

6. **How many characters are in the basic ASCII character set? How many bits are required to represent an ASCII character value?** 

   There are 128 characters in the set that are encoded into seven-bit integers.

7. **How many bytes are used to encode an ASCII value in UTF-8?**

   It takes one 8-bit byte to store each character.

8. **What is the UTF-8 encoding of your favorite emoji (provide the answer in hex)?**

   ```
   F0 9F 98 92
   ```

9. **Which character encoding is specified by the RFCs for HTTP/1.0 and HTTP/1.1?**

   HTTP uses the same definition of the term "character set" as that described for MIME which includes ASCII

10. **What line ending is used to delimit request and response headers in HTTP/1.0 and HTTP/1.1?**

    The ending used to delimit request and response headers is a LWS or linear white space.

