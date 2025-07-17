### 🚀 Basic Network Scanner (Port Scanner)
This repository contains a simple, multi-threaded Python-based network scanner designed to identify open ports on a target IP address within a specified range. It's a foundational project for anyone starting in cybersecurity, network programming, or Python development.

### ✨ Features
Port Scanning: Scans a defined range of TCP ports on a target IP.

Multi-threaded: Uses Python's threading module to speed up the scanning process by checking multiple ports concurrently.

Customizable Range: Allows users to specify the start and end ports for the scan.

Timeout Handling: Includes a timeout for connection attempts to avoid hanging on unresponsive ports.

Basic Input Validation: Handles command-line arguments and interactive user input.

Hostname Resolution: Can resolve hostnames to IP addresses before scanning.

### ⚙️ How It Works
The scanner operates by attempting to establish a TCP connection to each port in the specified range on the target IP address.

Socket Creation: For each port, a new socket object is created (configured for IPv4 and TCP).

Connection Attempt: The connect_ex() method is used, which returns 0 if the connection is successful (indicating an open port) or an error code otherwise.

Timeout: A short timeout is set for each connection attempt to prevent the scanner from getting stuck on filtered or closed ports.

Multi-threading: To enhance performance, separate threads are spawned for each port or a group of ports, allowing simultaneous connection attempts.

Result Reporting: Open ports are collected and displayed to the user upon completion of the scan.

### 🚀 Getting Started
Follow these steps to get your basic network scanner up and running.

Prerequisites
You'll need Python 3.x installed on your system.

Download Python

Installation
Clone the repository:

Bash
```
git clone https://github.com/RagulRM/basic-network-scanner.git
cd basic-network-scanner
```

Usage
You can run the script from your terminal.

Interactive Mode (No Arguments)
If you run the script without any command-line arguments, it will prompt you for the target IP address and port range.

Bash
```
python port_scanner.py
Example interaction:

Enter target IP address (default: 127.0.0.1): 192.168.1.1
Enter start port (default: 1): 1
Enter end port (default: 1024): 100
Command-Line Arguments
You can also provide the target IP and port range directly as arguments.
```

Bash
```
python port_scanner.py <target_ip> [start_port] [end_port]
<target_ip>: The IP address or hostname to scan (e.g., 127.0.0.1, example.com).

[start_port]: (Optional) The starting port number for the scan (default: 1).

[end_port]: (Optional) The ending port number for the scan (default: 1024).

Examples:

Scan localhost (ports 1-1024):
```
Bash
```
python port_scanner.py 127.0.0.1
Scan 192.168.1.1 (ports 1-1024):
```
Bash
```
python port_scanner.py 192.168.1.1
Scan example.com (ports 80-100):
```
Bash
```
python port_scanner.py example.com 80 100
```
### 🛠️ Code Structure
port_scanner.py:

is_port_open(target_ip, port, timeout): Attempts to connect to a single port and returns True if open.

scan_port(target_ip, port, open_ports, lock): Worker function for threads, calls is_port_open and adds to shared list.

run_port_scanner(target_ip, start_port, end_port): Orchestrates the multi-threaded scanning process.

Main block (if __name__ == "__main__":): Handles argument parsing and initiates the scan.

### 💡 Future Enhancements
This project is a great starting point! Here are some ideas to expand its functionality:

Service Banner Grabbing: Attempt to retrieve information about the service running on open ports (e.g., HTTP server version).

OS Detection: Implement techniques to guess the operating system of the target.

ARP Scanning: Add functionality to discover hosts on the local network using ARP requests.

UDP Scanning: Extend to scan for open UDP ports (more complex due to connectionless nature).

Output to File: Save scan results to a text file or a CSV.

GUI Interface: Develop a simple graphical user interface using libraries like Tkinter or PyQt.

Error Handling: Implement more robust error handling for network issues and invalid inputs.

Stealthier Scans: Explore different scan types (e.g., SYN scans using Scapy for more advanced users).

### 🤝 Contributing
Contributions are always welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

Fork the repository.

Create a new branch (git checkout -b feature/AmazingFeature).

Make your changes.

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

### 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
