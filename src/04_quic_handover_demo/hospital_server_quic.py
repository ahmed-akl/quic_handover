"""
hospital_server_quic.py

Purpose
-------
The "hospital" side of the real QUIC experiment. Uses the aioquic
library to run an actual QUIC server (TLS-encrypted, over UDP) that
receives patient heartbeat data and measures disruption gaps, exactly
like hospital_server_v2.py did for plain TCP - but this time over QUIC.

No code changes are needed here to support connection migration: QUIC's
ability to keep a session alive across an address change is handled
automatically by the protocol/library on the server side. All the
"handover" logic lives on the ambulance (client) side - see
ambulance_client_migration.py in this same folder.

Requirements
------------
Run generate_certificate.py once first (in this same folder) to create
cert.pem and key.pem, which this server loads on startup.

Run with: py hospital_server_quic.py
Pairs with: ambulance_client_migration.py (in the same folder).
"""
import asyncio
import time
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived

last_received_time = None
DISRUPTION_THRESHOLD = 1.5  # seconds


class HospitalProtocol(QuicConnectionProtocol):
    """
    aioquic protocol subclass representing the hospital's view of a
    single QUIC connection. aioquic calls quic_event_received()
    automatically whenever something happens on the connection (data
    arriving, the connection closing, etc.).
    """

    def quic_event_received(self, event):
        """
        Handle a single QUIC event delivered by aioquic.

        Parameters
        ----------
        event : aioquic.quic.events.QuicEvent
            The event object. This handler only acts on
            StreamDataReceived events (i.e. actual application data
            arriving); all other event types are ignored.
        """
        global last_received_time

        if isinstance(event, StreamDataReceived):
            current_time = time.time()

            if last_received_time is not None:
                gap = current_time - last_received_time
                if gap > DISRUPTION_THRESHOLD:
                    print(f"\u26a0\ufe0f  Disruption detected! Duration: {gap:.2f} seconds")

            print(f"Received: {event.data.decode()}")
            last_received_time = current_time


async def main():
    """
    Configure and start the QUIC server, then run forever, waiting for
    the ambulance client to connect and stream data.
    """
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain("cert.pem", "key.pem")

    print("Hospital (QUIC) is ready, waiting for ambulance connection...")

    await serve(
        "127.0.0.1",
        4433,
        configuration=configuration,
        create_protocol=HospitalProtocol,
    )
    await asyncio.Future()  # keep running forever


if __name__ == "__main__":
    asyncio.run(main())
