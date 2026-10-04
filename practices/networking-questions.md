# Networking Practice: Core Questions

A collection of active-recall questions designed to test and solidify computer networking fundamentals.

---

## 1. Web Protocols & Application Layer

- [ ] **1. What happens exactly when you type a URL into a browser and press enter?**
  - *Reference:* [RFC 7230 - HTTP/1.1 Message Syntax](https://datatracker.ietf.org/doc/html/rfc7230) | [MDN - How the Web Works](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works)
  - *Solution:* [Solution Notes](./solutions/q1-url-breakdown.md)

- [ ] **2. A customer's website is throwing a 502 Bad Gateway error. How do you troubleshoot this step-by-step?**
  - *Reference:* [MDN - 502 Bad Gateway](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/502) | [Nginx Docs - Proxy Pass](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
  - *Solution:* [Solution Notes](./solutions/q2-troubleshooting-502.md)

- [ ] **3. Why do HTTP, SMTP, and IMAP run on top of TCP rather than UDP?**
  - *Reference:* [RFC 9293 - Transmission Control Protocol (TCP)](https://datatracker.ietf.org/doc/html/rfc9293)
  - *Solution:* [Solution Notes](./solutions/q3-tcp-vs-udp-protocols.md)

- [ ] **4. Does TLS operate at the transport layer or application layer? What must a developer do to enhance TCP with TLS?**
  - *Reference:* [RFC 8446 - The Transport Layer Security (TLS) Protocol v1.3](https://datatracker.ietf.org/doc/html/rfc8446)
  - *Solution:* [Solution Notes](./solutions/q4-tls-layer-implementation.md)

- [ ] **5. Can you configure a browser for multiple simultaneous connections? What are the advantages and disadvantages?**
  - *Reference:* [RFC 9113 - HTTP/2 Multiplexing](https://datatracker.ietf.org/doc/html/rfc9113)
  - *Solution:* [Solution Notes](./solutions/q5-simultaneous-tcp-connections.md)

- [ ] **6. What are the advantages and disadvantages of TCP's byte-stream API vs. UDP's message boundary preservation?**
  - *Reference:* [RFC 768 - User Datagram Protocol](https://datatracker.ietf.org/doc/html/rfc768)
  - *Solution:* [Solution Notes](./solutions/q6-byte-stream-vs-message-boundaries.md)

---

## 2. Transport Layer & System Architecture

- [ ] **7. List the four broad classes of transport services and indicate whether TCP, UDP, or both provide them.**
  - *Reference:* [Kurose & Ross - Transport Layer Services](https://cgi.di.uoa.gr/~mema/courses/appnets/ComputerNetworking7thEdition.pdf)
  - *Solution:* [Solution Notes](./solutions/q7-transport-service-classes.md)

- [ ] **8. What is the fundamental difference between network architecture and application architecture?**
  - *Reference:* [OSI Model Overview - ISO/IEC 7498-1](https://www.iso.org/standard/20269.html)
  - *Solution:* [Solution Notes](./solutions/q8-network-vs-app-architecture.md)

- [ ] **9. How does ARP resolve an IP address to a MAC address inside a local subnet?**
  - *Reference:* [RFC 826 - An Ethernet Address Resolution Protocol](https://datatracker.ietf.org/doc/html/rfc826)
  - *Solution:* [Solution Notes](./solutions/q9-arp-resolution.md)

---

## 3. IP Addressing, Subnetting & Diagnostics

- [ ] **10. Given the subnet `192.168.1.0/26`, calculate the network address, broadcast address, and total usable host IPs.**
  - *Reference:* [RFC 4632 - Classless Inter-Domain Routing (CIDR)](https://datatracker.ietf.org/doc/html/rfc4632)
  - *Solution:* 

- [ ] **11. What is the difference between a public IP, private IP (RFC 1918), and NAT (Network Address Translation)?**
  - *Reference:* [RFC 1918 - Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918) | [RFC 3022 - Traditional NAT](https://datatracker.ietf.org/doc/html/rfc3022)
  - *Solution:* [Solution Notes](./solutions/q10-ip-types-and-nat.md)

- [ ] **12. What Linux CLI commands would you use to diagnose a DNS failure versus a physical gateway connectivity failure?**
  - *Reference:* [Linux man page: dig(1)](https://man7.org/linux/man-pages/man1/dig.1.html) | [Linux man page: ip-route(8)](https://man7.org/linux/man-pages/man8/ip-route.8.html)
  - *Solution:* [Solution Notes](./solutions/q11-dns-vs-gateway-diagnostics.md)


# Networking Practice: Projects

Hands-on socket programming and networking projects built with pure Python (no external dependencies required).

---

- [ ] **1. Single-Threaded HTTP Web Server**
  - **Overview:** Build a low-level HTTP web server using Python's `socket` library. The server listens for incoming HTTP requests, parses the requested file path (e.g., `/index.html`), serves the file with proper `200 OK` HTTP headers, or returns a formatted `404 Not Found` response if the file does not exist.
  - *Reference:* [RFC 7230 - HTTP/1.1 Message Syntax & Routing](https://datatracker.ietf.org/doc/html/rfc7230)
  - *Project Directory:* [`../projects/networking/01-http-web-server`](../projects/networking/01-http-web-server/readme.md)

- [ ] **2. UDP Client Ping & Round Trip Time (RTT) Calculator**
  - **Overview:** Build a UDP client/server pair that sends 10 ping messages over UDP to calculate packet loss and Round Trip Time (RTT) in milliseconds using precise timestamps. Implement socket timeouts (`settimeout`) to cleanly handle lost packets without freezing execution.
  - *Reference:* [RFC 768 - User Datagram Protocol](https://datatracker.ietf.org/doc/html/rfc768)
  - *Project Directory:* [`../projects/networking/02-udp-ping-client`](../projects/networking/02-udp-ping-client/readme.md)

- [ ] **3. HTTP Forward Proxy Server**
  - **Overview:** Develop a local HTTP proxy server that intercepts client browser requests, parses the target Host header, establishes a secondary outbound TCP connection to the origin web server, forwards the request, and pipes the origin server's HTTP response back to the client.
  - *Reference:* [RFC 7230 - Section 2.3: Proxies and Gateways](https://datatracker.ietf.org/doc/html/rfc7230#section-2.3)
  - *Project Directory:* [`../projects/networking/03-http-proxy-server`](../projects/networking/03-http-proxy-server)

- [ ] **4. HTTP Error Code Simulator (502, 503, 504)**
  - **Overview:** Build an interactive HTTP service designed to simulate exact server-side failure modes. Route distinct endpoints (`/502`, `/503`, `/504`) to return raw HTTP status lines and custom HTML diagnostic pages to practice recognizing and debugging upstream server failures.
  - *Reference:* [MDN - HTTP Response Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
  - *Project Directory:* [`../projects/networking/04-http-error-simulator`](../projects/networking/04-http-error-simulator)

- [ ] **5. Scheduled Server Uptime Test Suite**
  - **Overview:** Write a Python test suite using standard assertions or the `unittest` framework to test a server with scheduled availability windows (e.g., UP for $X$ seconds, DOWN for $Y$ seconds) to verify network connection error handling and socket timeout behaviors.
  - *Reference:* [Python Docs - `socket.connect_ex` and error codes](https://docs.python.org/3/library/socket.html#socket.socket.connect_ex)
  - *Project Directory:* [`../projects/networking/05-server-uptime-tests`](../projects/networking/05-server-uptime-tests)