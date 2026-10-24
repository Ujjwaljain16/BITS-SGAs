# Simple HTTP Client in C

Network Programming: Client-Server Programming  
Student Name: UJJWAL JAIN  
Student ID: 2024EB02528  
Institution: BITS Pilani  

## Overview
This project implements a standard HTTP client in C using POSIX BSD sockets to communicate with any HTTP server given either an IP address or domain hostname.

## Program Structure
The client adheres to the mandatory function declarations:
1. `int create_socket_and_connect(const char *hostname)`: Resolves hostnames/IP addresses using `getaddrinfo` with `AF_UNSPEC` and connects to port 80 with non-blocking timeout handling.
2. `void send_http_get_request(int sockfd, const char *hostname, const char *path)`: Constructs and transmits an HTTP/1.0 GET request with Host and User-Agent headers.
3. `void receive_http_response(int sockfd)`: Iteratively reads and prints the server response headers and body until EOF, reporting total bytes received.
4. `void interact_with_server(const char *hostname, const char *path)`: Coordinates the end-to-end socket lifecycle (connect, send, receive, close).
5. `int main(int argc, char *argv[])`: Validates command-line arguments, parses URL prefixes if present, and initiates server interaction.

## Compilation
To compile the client using gcc:
```bash
make
```
Or directly:
```bash
gcc -Wall -Wextra -O2 http_client.c -o client
```

## Usage
```bash
./client <hostname_or_ip> [path]
```

### Examples
1. Standard hostname:
   ```bash
   ./client example.com
   ```
2. Specific path query:
   ```bash
   ./client httpbin.org /get
   ```
3. Raw IP address:
   ```bash
   ./client 127.0.0.53
   ```

## Deliverables
- `http_client.c`: Source code with student credentials
- `2024EB02528_UJJWAL_JAIN_NP_Assignment.docx`: Formatted report with design details, function specifications, error matrix, and 8 test case runs
- `2024EB02528_UJJWAL_JAIN_NP_Assignment.pdf`: 10-page publication-quality PDF report
- `2024EB02528_UJJWAL_JAIN_NP_Assignment.zip`: Submission archive ready for upload
