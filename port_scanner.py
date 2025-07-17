import socket
import sys
import threading
from datetime import datetime

# --- Configuration ---
# You can modify these values for your scanning needs.
DEFAULT_TARGET_IP = "127.0.0.1"  # Default to localhost for safe testing
DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 1024  # Common ports to scan
SCAN_TIMEOUT = 1  # Timeout in seconds for socket connection attempts

# --- Helper Functions ---

def is_port_open(target_ip, port, timeout):
    """
    Checks if a specific port on a target IP is open.

    Args:
        target_ip (str): The IP address of the target.
        port (int): The port number to check.
        timeout (float): The timeout for the connection attempt in seconds.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    # Create a new socket object using IPv4 and TCP
    # AF_INET specifies the address family (IPv4)
    # SOCK_STREAM specifies the socket type (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)  # Set a timeout for the connection attempt

    try:
        # Attempt to connect to the target IP and port
        # connect_ex() returns an error indicator instead of raising an exception
        # 0 indicates success (port is open), otherwise it's an error code
        result = s.connect_ex((target_ip, port))
        if result == 0:
            return True
        else:
            return False
    except socket.gaierror:
        # Handles cases where the hostname could not be resolved
        print(f"Hostname could not be resolved. Exiting.")
        return False
    except socket.error as e:
        # Handles general socket errors (e.g., network unreachable)
        print(f"Couldn't connect to server: {e}")
        return False
    finally:
        s.close()  # Always close the socket to free up resources

def scan_port(target_ip, port, open_ports, lock):
    """
    Scans a single port and adds it to the open_ports list if found open.

    Args:
        target_ip (str): The IP address of the target.
        port (int): The port number to scan.
        open_ports (list): A shared list to store open ports.
        lock (threading.Lock): A lock to synchronize access to open_ports.
    """
    if is_port_open(target_ip, port, SCAN_TIMEOUT):
        with lock:  # Acquire lock before modifying shared resource
            open_ports.append(port)
        print(f"Port {port} is open")
    # else:
        # print(f"Port {port} is closed or filtered") # Uncomment for verbose output

def run_port_scanner(target_ip, start_port, end_port):
    """
    Runs a multi-threaded port scanner on the specified target and port range.

    Args:
        target_ip (str): The IP address of the target.
        start_port (int): The starting port for the scan.
        end_port (int): The ending port for the scan.
    """
    print("-" * 50)
    print(f"Scanning Target: {target_ip}")
    print(f"Scanning Ports from {start_port} to {end_port}")
    print(f"Scan started at: {datetime.now()}")
    print("-" * 50)

    open_ports = []
    threads = []
    lock = threading.Lock() # Create a lock for thread-safe list modification

    # Iterate through the port range and create a thread for each port
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target_ip, port, open_ports, lock))
        threads.append(thread)
        thread.start() # Start the thread

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("-" * 50)
    print(f"Scan finished at: {datetime.now()}")
    print("-" * 50)

    if open_ports:
        print("\nOpen Ports Found:")
        for port in sorted(open_ports):
            print(f" - {port}")
    else:
        print("No open ports found in the specified range.")

# --- Main Execution Block ---
if __name__ == "__main__":
    # Get target IP from command line arguments or use default
    if len(sys.argv) > 1:
        target_ip_input = sys.argv[1]
    else:
        target_ip_input = input(f"Enter target IP address (default: {DEFAULT_TARGET_IP}): ")
        if not target_ip_input:
            target_ip_input = DEFAULT_TARGET_IP

    # Get port range from command line arguments or use defaults
    start_port_input = DEFAULT_START_PORT
    end_port_input = DEFAULT_END_PORT

    if len(sys.argv) > 3:
        try:
            start_port_input = int(sys.argv[2])
            end_port_input = int(sys.argv[3])
        except ValueError:
            print("Invalid port range. Using default ports.")
    else:
        try:
            start_port_str = input(f"Enter start port (default: {DEFAULT_START_PORT}): ")
            if start_port_str:
                start_port_input = int(start_port_str)

            end_port_str = input(f"Enter end port (default: {DEFAULT_END_PORT}): ")
            if end_port_str:
                end_port_input = int(end_port_str)
        except ValueError:
            print("Invalid port input. Using default ports.")

    # Basic validation for port range
    if not (1 <= start_port_input <= 65535 and 1 <= end_port_input <= 65535 and start_port_input <= end_port_input):
        print("Error: Invalid port range. Ports must be between 1 and 65535, and start port must be less than or equal to end port.")
        sys.exit(1)

    # Resolve hostname to IP address if a hostname is provided
    try:
        resolved_ip = socket.gethostbyname(target_ip_input)
    except socket.gaierror:
        print(f"Error: Hostname '{target_ip_input}' could not be resolved.")
        sys.exit(1)

    run_port_scanner(resolved_ip, start_port_input, end_port_input)