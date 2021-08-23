import select
import socket
import json
import mysql.connector
import sys

#HOST = '127.0.0.1' #this host is the standard IPv4 address for loopback interfaces (localhost)
PORT = 1028
list_sockets = []
users = {}
i = 0
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET means IPV4, SOCK_STREAM means TCP server
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #for ADDRESS ALREADY IN USE error, is now reusable
server_socket.bind(('', PORT))
server_socket.listen(5)
list_sockets.append(server_socket)

conn = 0
message = ''

mydb = mysql.connector.connect(
    host = HOST,
    user = "root",
    password = "Haganay0"
)

print(mydb)

while True:
    read_ready, write_ready, error = select.select(list_sockets, [], [], 0)
    for sok in read_ready:
        if sok == server_socket:
            conn, addr = server_socket.accept()
            list_sockets.append(conn)
            to_send = ("You are connected from: " + str(addr)).encode("UTF-8")
            conn.send(len(to_send).to_bytes(2, byteorder='big'))
            conn.send(to_send)
            print("New connection")
        else:
            try:
                data = sok.recv(1024)
                if data:
                    parsed = json.loads(data)
                    message = parsed['msg']
                    if message.startswith("#"):
                        users[message[1:].lower()] = conn
                        print("User " + message[1:] + " added")
                        to_send = ("Username is " + str(message[1:])).encode("UTF-8")
                        users[message[1:].lower()].send(len(to_send).to_bytes(2, byteorder='big'))
                        users[message[1:].lower()].send(to_send)
                    elif message.startswith("@"):
                        print(message)
                        to_send = (message[message.index(":")+1:].encode("UTF-8"))
                        users[message[1:message.index(":")].lower()].send(len(to_send).to_bytes(2, byteorder='big'))
                        users[message[1:message.index(":")].lower()].send(to_send)
                        print(users)
                        print(users[message[1:message.index(":")].lower()])
            except Exception as e:
                print(e)
                continue

