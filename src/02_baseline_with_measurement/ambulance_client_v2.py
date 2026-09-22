"""
ambulance_client_v2.py

Purpose
-------
Same role as the baseline ambulance_client.py (sends simulated heartbeat
data once per second over plain TCP), but adds a deliberate pause after
the 10th message to simulate the ambulance entering a weak-signal /
dead-zone area (e.g. a tunnel) for 5 seconds before resuming.

Note on what this does and does NOT prove
-------------------------------------------
This version only pauses sending - it does NOT close the connection or
change the local port. It is a simple first look at "what does a gap in
data look like on the receiving end", used before moving to the more
realistic handover simulation in the 03_tcp_handover_demo and
04_quic_handover_demo folders, which actually change the local port to
simulate a real network/address change.

Run with: py ambulance_client_v2.py
Pairs with: hospital_server_v2.py (in the same folder), which measures
and prints the disruption duration automatically.
"""
import socket
import time

HOST = "127.0.0.1"
PORT = 5000

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

        # Simulate entering a dead zone after 10 messages
        if counter == 10:
            print(">>> Entering weak-signal area... pausing 5 seconds <<<")
            time.sleep(5)
            print(">>> Signal recovered, resuming transmission <<<")

        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped sending (Ctrl+C pressed).")

client.close()
