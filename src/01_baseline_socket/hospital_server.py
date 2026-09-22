"""
hospital_server.py

Purpose
-------
The very first, simplest prototype of the "hospital" side of the system.
It represents the hospital device that waits for the ambulance to connect
and prints every piece of patient data it receives.

This version uses a plain TCP socket (Python's built-in `socket` module) -
no QUIC yet. It exists to prove that basic two-way communication between
an "ambulance" and a "hospital" process works before adding any protocol
complexity on top.

How it fits in the project
---------------------------
This is step 1 of the prototype build-up described in the project report:
"build the simplest working baseline before adding measurement, then
before adding QUIC, then before adding migration simulation."

Run with: py hospital_server.py
(Must be started BEFORE ambulance_client.py, since the server needs to
be listening first.)
"""
import socket

HOST = "127.0.0.1"  # "this same computer" - loopback address
PORT = 5000          # arbitrary port number both sides must agree on

# Create a TCP socket and start listening for one incoming connection.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Hospital is ready, waiting for ambulance connection...")

conn, addr = server.accept()
print(f"Ambulance connected! From address: {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        # An empty bytes object means the other side closed the connection.
        break
    print(f"Received data: {data.decode()}")

conn.close()
