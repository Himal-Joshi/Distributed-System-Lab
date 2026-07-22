import socket
import os
import json
import threading

# Server Configuration
HOST = '127.0.0.1'
PORT = 5000
STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server_storage')

# Ensure server storage directory exists
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def handle_client(client_socket, address):
    print(f"[+] Client connected from {address[0]}:{address[1]}")
    
    while True:
        try:
            # Receive request data from client
            raw_data = client_socket.recv(4096).decode('utf-8')
            if not raw_data:
                break

            request = json.loads(raw_data)
            action = request.get("action", "").upper()
            filename = request.get("filename", "")
            content = request.get("content", "")

            response = {"status": "ERROR", "message": "Invalid Action", "data": None}

            # Sanitize filename to prevent directory traversal
            safe_filename = os.path.basename(filename) if filename else ""
            filepath = os.path.join(STORAGE_DIR, safe_filename) if safe_filename else ""

            # 1. CREATE File
            if action == "CREATE":
                if not safe_filename:
                    response = {"status": "ERROR", "message": "Filename required."}
                elif os.path.exists(filepath):
                    response = {"status": "ERROR", "message": f"File '{safe_filename}' already exists."}
                else:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    response = {"status": "SUCCESS", "message": f"File '{safe_filename}' created successfully."}

            # 2. READ File
            elif action == "READ":
                if not os.path.exists(filepath):
                    response = {"status": "ERROR", "message": f"File '{safe_filename}' not found."}
                else:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        file_data = f.read()
                    response = {"status": "SUCCESS", "message": f"File '{safe_filename}' read successfully.", "data": file_data}

            # 3. WRITE File (Update / Overwrite)
            elif action == "WRITE":
                if not safe_filename:
                    response = {"status": "ERROR", "message": "Filename required."}
                else:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    response = {"status": "SUCCESS", "message": f"File '{safe_filename}' written successfully."}

            # 4. DELETE File
            elif action == "DELETE":
                if not os.path.exists(filepath):
                    response = {"status": "ERROR", "message": f"File '{safe_filename}' not found."}
                else:
                    os.remove(filepath)
                    response = {"status": "SUCCESS", "message": f"File '{safe_filename}' deleted successfully."}

            # 5. LIST Files
            elif action == "LIST":
                files = os.listdir(STORAGE_DIR)
                response = {"status": "SUCCESS", "message": "Files listed successfully.", "data": files}

            # Send JSON response back to client
            client_socket.sendall(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError:
            err_resp = {"status": "ERROR", "message": "Invalid JSON payload."}
            client_socket.sendall(json.dumps(err_resp).encode('utf-8'))
        except Exception as e:
            err_resp = {"status": "ERROR", "message": str(e)}
            client_socket.sendall(json.dumps(err_resp).encode('utf-8'))
            break

    print(f"[-] Client {address[0]}:{address[1]} disconnected.")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse address option to allow immediate restart of server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"==========================================")
    print(f" Distributed File System (DFS) Server")
    print(f" Running on {HOST}:{PORT}")
    print(f" Storage Path: {STORAGE_DIR}")
    print(f"==========================================")
    print("Waiting for client connections...\n")

    try:
        while True:
            client_socket, address = server_socket.accept()
            # Handle client requests in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down DFS Server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
