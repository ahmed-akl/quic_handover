"""
hospital_server_v2.py

Purpose
-------
Same role as the baseline hospital_server.py (receives patient data over
plain TCP), but adds automatic disruption measurement: it times the gap
between consecutive received messages, and whenever that gap is longer
than DISRUPTION_THRESHOLD seconds, it prints exactly how long the
disruption lasted.

This is the first version of the project that produces a real, numeric
result instead of just a visual "it looks paused" observation.

How it fits in the project
---------------------------
Step 2 of the build-up: once basic communication works (step 1), add the
ability to measure disruptions automatically, so later comparisons
(TCP vs QUIC) can be backed by numbers, not just descriptions.

Run with: py hospital_server_v2.py
Pairs with: ambulance_client_v2.py (in the same folder), which pauses
sending for a few seconds partway through, simulating the ambulance
entering a weak-signal area.
"""
import socket
import time

HOST = "127.0.0.1"
PORT = 5000
DISRUPTION_THRESHOLD = 1.5  # seconds - any gap longer than this counts as a disruption

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Hospital is ready, waiting for ambulance connection...")

conn, addr = server.accept()
print(f"Ambulance connected! From address: {addr}")

last_received_time = time.time()

while True:
    data = conn.recv(1024)
    if not data:
        break

    current_time = time.time()
    gap = current_time - last_received_time

    if gap > DISRUPTION_THRESHOLD:
        print(f"\u26a0\ufe0f  Disruption detected! Duration: {gap:.2f} seconds")

    print(f"Received: {data.decode()}")
    last_received_time = current_time

conn.close()
