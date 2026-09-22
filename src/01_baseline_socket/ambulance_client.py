"""
ambulance_client.py

Purpose
-------
The very first, simplest prototype of the "ambulance" side of the system.
It represents the ambulance device continuously sending simulated patient
vital signs (a fake heartbeat reading) to the hospital, once per second,
forever - exactly like a real ambulance would stream data for the whole
trip, not just once.

This version uses a plain TCP socket - no QUIC yet. See hospital_server.py
in this same folder for why this simple baseline exists.

Run with: py ambulance_client.py
(Run this AFTER hospital_server.py is already running and waiting.)

Press Ctrl+C to stop sending.
"""
import socket
import time

HOST = "127.0.0.1"  # the hospital server's address (same computer here)
PORT = 5000          # must match the port used in hospital_server.py

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to hospital. Sending patient data...")

counter = 0
try:
    while True:
        message = f"Heartbeat #{counter} - HR: 95 bpm - BP: 120/80"
        client.sendall(message.encode())
        print(f"Sent: {message}")
        counter += 1
        time.sleep(1)  # send one reading every second
except KeyboardInterrupt:
    print("Stopped sending (Ctrl+C pressed).")

client.close()
