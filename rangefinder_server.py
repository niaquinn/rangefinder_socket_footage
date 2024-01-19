# the server (actual sim side)

# pymavlink to talk to sim
from pymavlink import mavutil

# opencv to read camera input
import cv2 as cv

# socket shit
import socket, pickle, struct

# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.0.1'
print('host ip: ', host_ip)
port = 62713
socket_address = (host_ip, port)

# bind the socket
server_socket.bind(socket_address)

# listen on the socket
server_socket.listen(4)
print('listening at: ', socket_address)

# accept at the socket
while True:
    client_socket, addr = server_socket.accept()
    print('got connection from: ', addr)

    if client_socket:
        vid = cv.VideoCapture('')

        while(vid.isOpened()):
            img, frame = vid.read()
            a  = pickle.dumps(frame)
            message = struct.pack('Q', len(a)) + a
            client_socket.sendall(message)

            cv.imshow('transmitting video', frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()

