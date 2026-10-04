# Project 02: UDP Client Ping & RTT Calculator

An application-level UDP ping client and server pair built with pure Python sockets to measure round-trip latency and simulate packet loss.

---

## Project Overview

Unlike TCP, the User Datagram Protocol (UDP) is connectionless and does not guarantee packet delivery or ordering. 

This project demonstrates how application-level protocols built on UDP handle network unreliability using socket timeouts (`settimeout`). The client transmits sequential UDP ping requests containing timestamps, measures the Round Trip Time (RTT) in milliseconds, and calculates packet loss percentages.

---

## Objectives

- Work with UDP sockets using `socket.SOCK_DGRAM`.
- Transmit datagrams with `sendto()` and receive datagrams with `recvfrom()`.
- Handle dropped packets gracefully using `client_socket.settimeout()`.
- Calculate network performance metrics: minimum, maximum, and average RTT alongside packet loss rate.

---

## Repository Structure

```text
02-udp-ping-client/
├── server.py       # UDP echo server with simulated 30% packet loss
├── client.py       # UDP ping client and RTT statistics collector
└── README.md       # Project documentation
```

---

## How to Run & Test

#### Start the UDP Server
```bash
# Open Terminal 1 and start the listener: 
  python3 server.py

# Output:
 UDP Ping Server listening on 127.0.0.1:12000 ...
```

#### Run the Ping Client
```bash
# Open Terminal 2 and execute the client script:

python3 client.py

# Sample Output

Pinging 127.0.0.1:12000 with 10 UDP packets:

Reply from 127.0.0.1: seq=1 time=0.45 ms
Reply from 127.0.0.1: seq=2 time=0.38 ms
Request timed out for seq=3
Reply from 127.0.0.1: seq=4 time=0.41 ms
Reply from 127.0.0.1: seq=5 time=0.39 ms
Request timed out for seq=6
Reply from 127.0.0.1: seq=7 time=0.42 ms
Reply from 127.0.0.1: seq=8 time=0.37 ms
Reply from 127.0.0.1: seq=9 time=0.40 ms
Reply from 127.0.0.1: seq=10 time=0.44 ms

--- Ping Statistics ---
Packets: Sent = 10, Received = 8, Lost = 2 (20.0% loss)
RTT min/avg/max = 0.37 / 0.41 / 0.45 ms
```

## Key Takeaways

**Connectionless Communication:** UDP requires no handshake (`connect()` or `accept()`). Data packets are sent directly using destination IP and port tuples.

**Handling Unreliability:** Because UDP lacks native retransmissions, application code must implement timeouts (`socket.timeout`) to avoid blocking indefinitely when packets are dropped by network routers or remote hosts.