#!/usr/bin/env python3
import os
import sys
import subprocess
import signal
import time

def check_port(port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def kill_process_on_port(port):
    try:
        # Find process using the port
        cmd = f"lsof -t -i:{port}"
        pid = subprocess.check_output(cmd, shell=True).decode().strip()
        if pid:
            # Try graceful shutdown first
            os.kill(int(pid), signal.SIGTERM)
            time.sleep(2)  # Give it time to shutdown gracefully
            
            # Force kill if still running
            if check_port(port):
                os.kill(int(pid), signal.SIGKILL)
                time.sleep(1)
        return True
    except Exception as e:
        print(f"Error killing process: {e}")
        return False

def start_server():
    # Kill any existing process on port 5001
    if check_port(5001):
        print("Port 5001 in use, attempting to free...")
        if not kill_process_on_port(5001):
            print("Failed to free port 5001")
            return False
    
    # Start the server
    print("Starting server...")
    try:
        subprocess.run([sys.executable, "llmserver.py"])
        return True
    except KeyboardInterrupt:
        print("\nShutting down server...")
        return True
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

if __name__ == "__main__":
    start_server()