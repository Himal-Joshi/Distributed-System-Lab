import os
import sys
import time
import threading
import unittest

# Import server and client modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import server
import client

class TestDFS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start server in a background daemon thread
        cls.server_thread = threading.Thread(target=server.start_server, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5)  # Give server time to bind and listen

    def test_01_create_file(self):
        res = client.send_request("CREATE", "lab3_test.txt", "Hello DFS World!")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("created successfully", res["message"])

    def test_02_read_file(self):
        res = client.send_request("READ", "lab3_test.txt")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["data"], "Hello DFS World!")

    def test_03_write_file(self):
        res = client.send_request("WRITE", "lab3_test.txt", "Updated content for Distributed File System.")
        self.assertEqual(res["status"], "SUCCESS")
        
        # Verify read after write
        res_read = client.send_request("READ", "lab3_test.txt")
        self.assertEqual(res_read["data"], "Updated content for Distributed File System.")

    def test_04_list_files(self):
        res = client.send_request("LIST")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("lab3_test.txt", res["data"])

    def test_05_delete_file(self):
        res = client.send_request("DELETE", "lab3_test.txt")
        self.assertEqual(res["status"], "SUCCESS")

        # Verify read fails after delete
        res_read = client.send_request("READ", "lab3_test.txt")
        self.assertEqual(res_read["status"], "ERROR")

if __name__ == "__main__":
    unittest.main()
