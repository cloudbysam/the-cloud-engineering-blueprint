# Project 03: HTTP Forward Proxy Server

A lightweight HTTP forward proxy server built in pure Python using raw TCP sockets to intercept, inspect, and forward client web requests.

---

## Project Overview

An HTTP proxy acts as an intermediary node between a client (such as a web browser or API client) and an origin server. 

This project demonstrates how a proxy server parses incoming HTTP headers to extract target destination host details, establishes outbound TCP socket connections to origin web servers, and streams raw HTTP response payloads back to clients.

---

## Objectives

- Implement dual-socket proxying (`client_socket` for ingress, `origin_socket` for egress).
- Parse raw HTTP request headers to extract target `Host` headers and destination ports.
- Stream data bidirectionally over TCP socket streams.

---

## Repository Structure

```text
03-http-proxy-server/
├── proxy.py        # Forward proxy server script
└── README.md       # Project documentation
```

## How to Run & Test

```Bash
# 1. Start an Origin Server (Project 1)
In Terminal 1 (run a webserver an HTTP web server on port 8080)

python3 projects/networking/01-http-web-server/server.py

# 2. Start the Forward Proxy Server
In Terminal 2, start the proxy server on port 8888:

Bash
python3 projects/networking/03-http-proxy-server/proxy.py

# 3. Send Requests Through the Proxy
In Terminal 3, route requests through the proxy to target port 8080:

curl -i -H "Host: 127.0.0.1:8080" [http://127.0.0.1:8888/index.html](http://127.0.0.1:8888/index.html)
```

## Key Takeaways

**Intermediary Architecture:** Proxies maintain two independent socket lifecycle connections: one receiving data from the client, and one sending/receiving data from the origin server.

**Header Parsing:** Proxies must inspect incoming HTTP payloads to inspect Host: routing details before establishing outbound origin connections.