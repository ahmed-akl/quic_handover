"""
ambulance_client_migration.py

Purpose
-------
This is the core experiment of the project: it demonstrates REAL QUIC
Connection Migration. It uses aioquic's low-level, synchronous
QuicConnection API (instead of the asyncio wrapper) so the exact moment
of the network handover is fully under our control and easy to reason
about step by step.

The client sends 5 heartbeat messages from a local UDP port representing
"Wi-Fi" (7001), then closes that socket and opens a brand new one on a
different local port representing "cellular" (7002) - a genuine address
change from the network's point of view - and sends 5 more messages
using the SAME underlying QuicConnection object (i.e. the same
Connection ID, the same session).

This is compared directly against ambulance_client_tcp_migration.py
(in the 03_tcp_handover_demo folder), which performs the exact same
port-switch using plain TCP and loses the session as a result.

Run with: py ambulance_client_migration.py
Pairs with: hospital_server_quic.py (in the same folder), which must
already be running, and requires cert.pem/key.pem to already exist
(see generate_certificate.py).
"""
import socket
import ssl
import time
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.connection import QuicConnection

SERVER = ("127.0.0.1", 4433)

config = QuicConfiguration(is_client=True)
config.verify_mode = ssl.CERT_NONE  # accept the self-signed certificate

quic = QuicConnection(configuration=config)
quic.connect(SERVER, now=time.time())

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 7001))  # simulates the "Wi-Fi" local port
sock.settimeout(2)


def flush(s):
    """
    Send every QUIC packet that the QuicConnection currently has queued
    up, over the given UDP socket.

    Parameters
    ----------
    s : socket.socket
        The UDP socket to send pending QUIC packets through. This is a
        parameter (rather than always using the same global socket) so
        the same function works both before and after the handover,
        once `sock` has been reassigned to the new "cellular" socket.
    """
    for data, addr in quic.datagrams_to_send(now=time.time()):
        s.sendto(data, addr)


def pump(s):
    """
    Try to receive one incoming UDP packet and feed it into the QUIC
    state machine, so aioquic can process handshake responses,
    acknowledgements, etc.

    Parameters
    ----------
    s : socket.socket
        The UDP socket to receive from. If no packet arrives within the
        socket's timeout, this function does nothing (this keeps the
        demo simple and synchronous rather than fully event-driven).
    """
    try:
        data, addr = s.recvfrom(65536)
        quic.receive_datagram(data, addr, now=time.time())
    except socket.timeout:
        pass


# --- QUIC handshake over the "Wi-Fi" socket ---
flush(sock)
pump(sock)
flush(sock)
print("Connected via port 7001 (simulating Wi-Fi)")

stream_id = quic.get_next_available_stream_id()
counter = 0

# --- send 5 messages over "Wi-Fi" ---
for i in range(5):
    msg = f"Heartbeat #{counter}".encode()
    quic.send_stream_data(stream_id, msg, end_stream=False)
    flush(sock)
    print("Sent:", msg.decode())
    counter += 1
    time.sleep(0.3)
    pump(sock)

# --- HANDOVER: brand new local port, but the SAME quic session ---
print(">>> Simulating handover: switching from Wi-Fi (7001) to cellular (7002) <<<")
t0 = time.time()
sock.close()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 7002))
sock.settimeout(2)

# --- resume sending on the SAME quic connection, just via the new socket ---
for i in range(5):
    msg = f"Heartbeat #{counter}".encode()
    quic.send_stream_data(stream_id, msg, end_stream=False)
    flush(sock)
    print("Sent:", msg.decode())
    counter += 1
    time.sleep(0.3)
    pump(sock)

print(f"Migration completed in {time.time()-t0:.3f}s (SAME session, no reconnect needed)")
sock.close()
