# Project 01: Single-Threaded HTTP Web Server

A low-level, zero-dependency HTTP web server written in pure Python using raw TCP sockets.

---

##  Project Overview

This project demonstrates how web servers process HTTP requests at the socket level without relying on high-level web frameworks (like Flask or Django). 

The server listens on a local port, parses incoming HTTP `GET` request headers over TCP, serves local static files with proper `200 OK` status headers, and handles missing resources with a custom `404 Not Found` response.

---

## Objectives

- Understand the TCP lifecycle: `socket()`, `bind()`, `listen()`, `accept()`, `recv()`, `sendall()`, and `close()`.
- Parse raw HTTP/1.1 wire protocol messages.
- Handle basic web server file routing and error responses safely.

---

## Repository Structure

```text
01-http-web-server/
├── server.py       # Main Python socket server script
├── index.html      # Sample static HTML page to serve
└── README.md       # Project documentation