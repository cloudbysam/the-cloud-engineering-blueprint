import socket

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8888

# 1. Start the proxy server socket
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))
proxy_socket.listen(5)

print(f"HTTP Forward Proxy running on http://{PROXY_HOST}:{PROXY_PORT} ...")

while True:
    # Accept connection from client (e.g., browser or curl)
    client_socket, client_addr = proxy_socket.accept()
    print(f"\n[+] Intercepted connection from client: {client_addr}")

    # Receive client request
    request_data = client_socket.recv(4096)
    if not request_data:
        client_socket.close()
        continue

    # Decode request headers to find the target host
    request_text = request_data.decode('utf-8', errors='ignore')
    first_line = request_text.split('\r\n')[0]
    print(f"[>] Request Line: {first_line}")

    # Extract target host from Host header
    target_host = None
    target_port = 80  # Default HTTP port

    for line in request_text.split('\r\n'):
        if line.lower().startswith("host:"):
            host_header = line.split(":", 1)[1].strip()
            if ":" in host_header:
                target_host, port_str = host_header.split(":")
                target_port = int(port_str)
            else:
                target_host = host_header
            break

    if not target_host:
        print("[!] Could not determine target Host header. Closing connection.")
        client_socket.close()
        continue

    print(f"[*] Forwarding request to target server -> {target_host}:{target_port}")

    try:
        # 2. Create outbound socket to target origin server
        origin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        origin_socket.connect((target_host, target_port))

        # Forward the client's raw request directly to origin
        origin_socket.sendall(request_data)

        # 3. Receive response from origin server and pipe it back to client
        while True:
            response_data = origin_socket.recv(4096)
            if len(response_data) > 0:
                client_socket.sendall(response_data)
            else:
                break  # Origin closed connection

        origin_socket.close()
        print(f"[<] Response successfully relayed back to client.")

    except Exception as e:
        print(f"[!] Error proxying request: {e}")

    client_socket.close()
    