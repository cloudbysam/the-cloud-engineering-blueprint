# Transmission Control Protocol (TCP)
The Transmission Control Protocol (TCP) is a transport layer protocol that offers **reliable communication** between the sender & receiver with the capability of retransmitting data in case of packet loss. Communication via TCP is initiated between the sender and receiver via a three-way handshake process. 

The three-way handshake process is an agreement between the two parties to establish a connection:
- **Client sends SYN:** "I want to talk."
- **Server sends SYN-ACK:** "I heard you, and I want to talk too."
- **Client sends ACK:** "Confirmed, let's start."

# User Datagram Protocol (UDP)
Some business use cases where latency is more critical than packet loss include voice and video calls, live event streaming, gaming, and DNS. The UDP transport protocol is less reliable but faster than TCP and works well for these use cases. It is faster because it does not require a three-way handshake to establish a connection, and it provides no guarantee of data delivery.

## TCP/IP vs. TCP
It is important to understand the difference between these two, as it is easy to mix them up:
- **TCP/IP** is a complete four-layer conceptual framework that dictates how data moves across the internet from one host to another.
- **TCP** is a specific protocol residing at the **Transport Layer** of that framework. When an application sends data over TCP/IP, it chooses a delivery method at the Transport Layer—typically TCP or UDP.

---

## TCP vs. UDP Core Comparison

| Metric | TCP | UDP |
| :--- | :--- | :--- |
| **Connection Type** | Connection-oriented (3-way handshake required). | Connectionless (fire and forget). |
| **Reliability** | Guaranteed delivery (retransmits dropped data). | Best-effort delivery (dropped data is lost). |
| **Data Ordering** | Strict sequencing (arrives in exact sent order). | No sequencing (packets can arrive out of order). |
| **Data Flow** | Continuous byte stream (`SOCK_STREAM`). | Discrete datagram packets (`SOCK_DGRAM`). |


## Common Network Connection Errors

| Error Name / Code | Transport Protocol | Common Cause | Python Exception |
| :--- | :--- | :--- | :--- |
| **Connection Refused**<br>`ECONNREFUSED` | **TCP** | Target IP/host is reachable, but no process is actively listening on the target port (or blocked by firewall/security group). | `ConnectionRefusedError`<br>*(Errno 111 / 10061)* |
| **Connection Timed Out**<br>`ETIMEDOUT` | **TCP & UDP** | Network path is down, target host is powered off, or silent firewall drops packets without returning a `RST` or `ICMP`. | `TimeoutError` / `socket.timeout`<br>*(Errno 110 / 10060)* |
| **Connection Reset by Peer**<br>`ECONNRESET` | **TCP** | Remote host abruptly killed the TCP session (e.g., server process crashed, rebooted, or sent an unexpected `RST` packet). | `ConnectionResetError`<br>*(Errno 104 / 10054)* |
| **Host / Network Unreachable**<br>`EHOSTUNREACH` / `ENETUNREACH` | **TCP & UDP** | Routing failure—local machine or an intermediate router cannot find a valid network route to the destination IP address. | `OSError`<br>*(Errno 113 / 10065)* |
| **Address Already in Use**<br>`EADDRINUSE` | **TCP & UDP** | Server attempt to `bind()` to a port that is already occupied by another running process (or in `TIME_WAIT` state without `SO_REUSEADDR`). | `OSError`<br>*(Errno 98 / 10048)* |
| **Broken Pipe**<br>`EPIPE` | **TCP** | Client or server attempts to write/send data to a TCP connection that the other side has already closed. | `BrokenPipeError`<br>*(Errno 32 / 10032)* |
| **Port Unreachable (ICMP)** | **UDP** | Sender transmitted a UDP datagram to a port where no socket is bound; target host replies with an `ICMP Port Unreachable` message. | `ConnectionRefusedError`<br>*(Or silent loss depending on OS)* |