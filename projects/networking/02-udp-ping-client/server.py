import random
import socket

HOST = '127.0.0.1'
PORT = 12000

# Create a UDP socket (AF_INET = IPv4, SOCK_DGRAM = UDP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP Ping Server listening on {HOST}:{PORT} ...")

while True:
    # Receive UDP packet (data and client address)
    data, address = server_socket.recvfrom(1024)
    message = data.decode('utf-8')

    # Simulate 30% packet loss artificially
    if random.randint(1, 10) <= 3:
        print(f"[DROPPED] Simulated packet loss for request: {message.strip()}")
        continue

    # Echo back a PONG response to the client
    response = f"PONG: {message}"
    server_socket.sendto(response.encode('utf-8'), address)
    print(f"[REPLIED] Sent response to {address}: {response.strip()}")