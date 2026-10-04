import socket
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12000

# 1. Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Set socket timeout to 1.0 second
# If recvfrom() waits longer than 1 second, it raises socket.timeout
client_socket.settimeout(1.0)

# Track stats
rtts = []
packets_sent = 10
packets_received = 0

print(f"Pinging {SERVER_HOST}:{SERVER_PORT} with 10 UDP packets:\n")

for sequence_number in range(1, packets_sent + 1):
    # Capture timestamp right before sending
    send_time = time.time()
    
    # Message format: "PING <seq> <timestamp>"
    message = f"PING {sequence_number} {send_time}"

    try:
        # Send packet over UDP
        client_socket.sendto(message.encode('utf-8'), (SERVER_HOST, SERVER_PORT))

        # Wait for reply
        data, server_address = client_socket.recvfrom(1024)
        
        # Capture timestamp immediately upon receipt
        receive_time = time.time()
        
        # Calculate RTT in milliseconds
        rtt_ms = (receive_time - send_time) * 1000
        rtts.append(rtt_ms)
        packets_received += 1

        print(f"Reply from {server_address[0]}: seq={sequence_number} time={rtt_ms:.2f} ms")

    except socket.timeout:
        # Fired if 1.0 second passes without a response
        print(f"Request timed out for seq={sequence_number}")

# Clean up socket
client_socket.close()

# Summary Statistics
loss_rate = ((packets_sent - packets_received) / packets_sent) * 100
print("\n--- Ping Statistics ---")
print(f"Packets: Sent = {packets_sent}, Received = {packets_received}, Lost = {packets_sent - packets_received} ({loss_rate:.1f}% loss)")

if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = sum(rtts) / len(rtts)
    print(f"RTT min/avg/max = {min_rtt:.2f} / {avg_rtt:.2f} / {max_rtt:.2f} ms")