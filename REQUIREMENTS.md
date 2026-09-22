# System Requirements

## 1. What the application should do

The application simulates an ambulance sending live patient vital-sign
data (heart rate, blood pressure) to a hospital, while the ambulance
moves between different networks (e.g. Wi-Fi to cellular). The goal is
to compare two network protocols — **TCP** (traditional) and **QUIC**
(modern) — and measure which one keeps the data connection alive when
the ambulance's network address changes mid-transmission.

The end goal is to show that QUIC's **Connection Migration** feature
allows the hospital to keep receiving data continuously during a
network handover, while plain TCP loses the connection and must start
over.

## 2. Implemented functionalities

- [x] Basic two-way communication between an "ambulance" (client) and a
      "hospital" (server) process, using plain TCP sockets.
- [x] Automatic measurement of disruption time: the hospital server
      detects and prints the gap (in seconds) whenever data stops
      arriving for longer than a threshold.
- [x] A real TCP handover simulation: the ambulance client closes its
      connection and reconnects from a different local port mid-session,
      simulating a Wi-Fi → cellular switch. This proves TCP treats the
      new connection as an entirely new, unrelated session.
- [x] A real QUIC server and client, built using the `aioquic` library,
      with a self-signed TLS certificate generated locally.
- [x] A real QUIC handover simulation: the ambulance client switches to
      a brand new local UDP port mid-session (same kind of change as
      the TCP test), while keeping the same underlying QUIC connection
      (same Connection ID). This demonstrates QUIC's Connection
      Migration working in practice — the hospital keeps receiving data
      without any reconnect.
- [x] Two comparison charts (generated with `matplotlib`):
  - A bar chart comparing number of sessions created and handover time
    for TCP vs QUIC.
  - A message-level timeline chart showing exactly where the TCP
    session breaks vs where the QUIC session stays continuous.

## 3. Missing / not-yet-implemented functionalities


- [ ] **Two-device test over a real Wi-Fi network.** All experiments so
      far run on a single machine using loopback addresses
      (`127.0.0.1`) with different local ports simulating different
      networks. A real two-device test (ambulance laptop + hospital
      laptop on the same Wi-Fi network, using real local IP addresses)
      has been planned but not completed yet.

