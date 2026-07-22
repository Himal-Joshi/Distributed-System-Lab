import socket
import json

# Server Connection Details (hardcoded as per requirements)
HOST = '127.0.0.1'
PORT = 5000

def send_request(action, filename="", content=""):
    """
    Sends a request dictionary to the DFS Server and receives the response.
    """
    try:
        # Create TCP Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        payload = {
            "action": action,
            "filename": filename,
            "content": content
        }

        # Send JSON payload
        client_socket.sendall(json.dumps(payload).encode('utf-8'))

        # Receive JSON response
        raw_response = client_socket.recv(4096).decode('utf-8')
        response = json.loads(raw_response)

        client_socket.close()
        return response

    except ConnectionRefusedError:
        return {"status": "ERROR", "message": "Could not connect to DFS Server. Is server.py running?"}
    except Exception as e:
        return {"status": "ERROR", "message": f"Connection error: {str(e)}"}

def main():
    while True:
        print("\n==========================================")
        print("    DISTRIBUTED FILE SYSTEM (DFS) CLIENT   ")
        print("==========================================")
        print("1. Create File")
        print("2. Read File")
        print("3. Write / Update File")
        print("4. Delete File")
        print("5. List Files")
        print("6. Exit")
        print("==========================================")
        
        choice = input("Enter option (1-6): ").strip()

        # 1. CREATE File
        if choice == '1':
            filename = input("Enter filename to create (e.g., test.txt): ").strip()
            if not filename:
                print("[!] Filename cannot be empty.")
                continue
            content = input("Enter initial file content (optional): ")
            response = send_request("CREATE", filename, content)
            print(f"\n[Server Status] : {response.get('status')}")
            print(f"[Server Message]: {response.get('message')}")

        # 2. READ File
        elif choice == '2':
            filename = input("Enter filename to read: ").strip()
            if not filename:
                print("[!] Filename cannot be empty.")
                continue
            response = send_request("READ", filename)
            print(f"\n[Server Status] : {response.get('status')}")
            print(f"[Server Message]: {response.get('message')}")
            if response.get("status") == "SUCCESS":
                print("------------------------------------------")
                print("FILE CONTENT:")
                print(response.get("data", ""))
                print("------------------------------------------")

        # 3. WRITE / Update File
        elif choice == '3':
            filename = input("Enter filename to write/update: ").strip()
            if not filename:
                print("[!] Filename cannot be empty.")
                continue
            content = input("Enter content to write: ")
            response = send_request("WRITE", filename, content)
            print(f"\n[Server Status] : {response.get('status')}")
            print(f"[Server Message]: {response.get('message')}")

        # 4. DELETE File
        elif choice == '4':
            filename = input("Enter filename to delete: ").strip()
            if not filename:
                print("[!] Filename cannot be empty.")
                continue
            response = send_request("DELETE", filename)
            print(f"\n[Server Status] : {response.get('status')}")
            print(f"[Server Message]: {response.get('message')}")

        # 5. LIST Files
        elif choice == '5':
            response = send_request("LIST")
            print(f"\n[Server Status] : {response.get('status')}")
            print(f"[Server Message]: {response.get('message')}")
            if response.get("status") == "SUCCESS":
                files = response.get("data", [])
                print("------------------------------------------")
                print("FILES ON DFS SERVER:")
                if files:
                    for idx, f in enumerate(files, 1):
                        print(f"  {idx}. {f}")
                else:
                    print("  (No files available)")
                print("------------------------------------------")

        # 6. EXIT
        elif choice == '6':
            print("\n[+] Exiting DFS Client. Goodbye!")
            break

        else:
            print("\n[!] Invalid choice. Please select an option between 1 and 6.")

if __name__ == "__main__":
    main()
