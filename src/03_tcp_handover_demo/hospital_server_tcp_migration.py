"""
hospital_server_tcp_migration.py

Purpose
-------
This is the "control group" experiment of the whole project: it proves,
with plain TCP, that a real network handover (the client switching to a
brand new local port, simulating a Wi-Fi -> cellular switch) is treated
as a completely new, unrelated session.

Every time a new TCP connection arrives, this server increments and
prints a session counter. If the ambulance client's handover produces
TWO separate "NEW SESSION" messages instead of one continuous session,
that is the experimental proof that TCP cannot survive an address change
without a full reconnect.

How it fits in the project
---------------------------
This result is directly compared against 04_quic_handover_demo, which
runs the exact same handover scenario using QUIC instead, to show QUIC's
Connection Migration keeping the session alive across the same kind of
change.

Run with: py hospital_server_tcp_migration.py
Pairs with: ambulance_client_tcp_migration.py (in the same folder).
"""
import socket

HOST = "127.0.0.1"
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print("Hospital (TCP) is ready, waiting for ambulance connection...")

session_number = 0
while True:
    conn, addr = server.accept()
    session_number += 1
    print(f"\n\u26a0\ufe0f  NEW SESSION #{session_number} started from {addr} "
          f"(previous session lost, if any)")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("Connection closed by client.")
                break
            print("Received:", data.decode())
    except Exception as e:
        print("Error:", e)
