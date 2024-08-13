#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 19:00:52 2022

@author: ulices
"""
import socket

UDP_IP = "192.168.0.230"
UDP_IP = "0.0.0.0"

UDP_PORT = 65432

#UDP_IP = "0.0.0.0"
#UDP_PORT = 51001


print("prepared")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

print("socket created")

sock.bind((UDP_IP, UDP_PORT))

print("binded")

#while True:
data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
print("received message:", data.decode("utf-8"))
print("received message: %s" % data)
sock.close()
