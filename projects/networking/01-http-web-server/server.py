import socket

# --- 1. SETUP THE SERVER ---
HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server running on http://{HOST}:{PORT} ...")

# --- 2. LISTEN AND PROCESS REQUESTS ---
while True:
    # Wait for browser connection
    client_socket, client_address = server_socket.accept()
    print(f"[+] Connection accepted from {client_address}")

    # Read up to 1024 bytes of incoming data
    request_data = client_socket.recv(1024).decode('utf-8')

    # Guard: handle empty browser requests
    if not request_data:
        client_socket.close()
        continue

    # --- 3. PARSE THE REQUEST ---
    first_line = request_data.split('\r\n')[0] 
    requested_path = first_line.split(' ')[1]  
    
    if requested_path == '/':
        filename = 'index.html'
    else:
        filename = requested_path.lstrip('/')

    print(f"Target file requested: {filename}")

    # --- 4. READ FILE & BUILD HTTP RESPONSE ---
    try:
        # Open and read the requested file
        with open(filename, 'r') as f:
            content = f.read()

        # Build 200 OK Response
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n" + 
            content
        )
    except FileNotFoundError:
        # Build 404 Not Found Response
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>404 Not Found</h1><p>The requested file does not exist.</p></body></html>"
        )

    # --- 5. SEND RESPONSE & CLOSE SOCKET ---
    # .sendall() requires raw bytes, so we encode string -> utf-8 bytes
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()