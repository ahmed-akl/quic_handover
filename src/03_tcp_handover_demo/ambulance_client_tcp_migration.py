"""
ambulance_client_tcp_migration.py

Purpose
-------
Simulates a real network handover using plain TCP: the client sends 5
heartbeat messages from a local port representing "Wi-Fi" (7001), then
DELIBERATELY closes that connection and opens a brand new one from a
different local port representing "cellular" (7002), and sends 5 more
messages.

This is the same handover event used in the QUIC experiment
(04_quic_handover_demo), so the two results are directly comparable.
The expected (and actual, observed) outcome is that the hospital server
sees this as two completely separate sessions - proving TCP has no way
to recognize "this is the same ambulance, just on a different network".

Run with: py ambulance_client_tcp_migration.py
Pairs with: hospital_server_tcp_migration.py (in the same folder), which
must already be running.
"""
import socket
import time

SERVER = ("127.0.0.1", 5001)


def new_connection(local_port):
    """
    Open a brand new TCP connection to the hospital server, forcing the
    connection to originate from a specific local port.

    Parameters
    ----------
    local_port : int
        The local port to bind this socket to before connecting. Using a
        different value each time simulates the ambulance device having
        a different local network address after a handover.

    Returns
    -------
    socket.socket
        A connected TCP socket ready to send data.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", local_port))
    s.connect(SERVER)
    return s


# --- connect via "Wi-Fi" port ---
client = new_connection(7001)
print("Connected via port 7001 (simulating Wi-Fi)")

counter = 0
for i in range(5):
    msg = f"Heartbeat #{counter}".encode()
    client.sendall(msg)
    print("Sent:", msg.decode())
    counter += 1
    time.sleep(0.3)

# --- HANDOVER: TCP cannot survive this - must fully reconnect ---
print(">>> Simulating handover: switching from Wi-Fi (7001) to cellular (7002) <<<")
t0 = time.time()
client.close()  # old connection is completely destroyed

client = new_connection(7002)  # brand new TCP handshake required
print(f"Reconnected via port 7002 in {time.time()-t0:.3f}s (NEW session, old one was lost)")

for i in range(5):
    msg = f"Heartbeat #{counter}".encode()
    client.sendall(msg)
    print("Sent:", msg.decode())
    counter += 1
    time.sleep(0.3)

client.close()
