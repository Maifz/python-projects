# Project 001

Create a syncroneous client-server chat application

## Server

* The server should listen on a TCP port configurable via command line arguments. (similar like netcat: `nc -l 4444`).
* Once a client connects to the server, a message should appear with IP address and time.
* A client must be able to connect to the server and send text line-wise (newline terminated)
* A message from a client must be prefixed by its IP address
* On the server you must be able to send messages back to the client
* The server should have a prefixed prompt when writing messages
* It should be visually clear who send and who received messages

## Client

* The client must be able to connect to a network TCP port configurable via command line arguments. (similar like netcat: `nc <host> <port>`)
* Once the client is connected, it should be visually acknowledged
* The client should be able to exchanged line-wise messages with the server
* The client should have a prefixed prompt when writing messages
* It should be visually clear who send and who received messages


## PR's

Code must be submitted within a subdirectory of this directory.
