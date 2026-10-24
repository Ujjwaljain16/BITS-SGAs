/*
 * ------------------------------------------------------------------
 *  Network Programming and Client Server Programming
 *  Assignment : Simple HTTP Client using sockets
 *
 *  Student Name : UJJWAL JAIN
 *  Student ID   : 2024EB02528
 *
 *  Build : gcc http_client.c -o client
 *  Usage : ./client <hostname | IP address> [path]
 *          e.g. ./client 127.0.0.53
 *               ./client neverssl.com /index.html
 * ------------------------------------------------------------------
 */

#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include <poll.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

#define SERVER_PORT        "80"
#define REQ_SIZE           2048
#define RECV_CHUNK         1024
#define CONNECT_TIMEOUT_MS 5000
#define READ_TIMEOUT_MS    10000

/*
 * create_socket_and_connect()
 * Input  : hostname - server name or IP address
 * Output : descriptor of a connected TCP socket
 * Resolves the host, creates a socket and connects to port 80.
 * Prints an error and terminates the program if this fails.
 */
int create_socket_and_connect(const char *hostname)
{
    struct addrinfo hints;
    struct addrinfo *list, *ai;
    int fd = -1;
    int rc, flags, last_err = 0;

    memset(&hints, 0, sizeof hints);
    hints.ai_family   = AF_UNSPEC;   /* IPv4 or IPv6, whatever the host has */
    hints.ai_socktype = SOCK_STREAM;

    rc = getaddrinfo(hostname, SERVER_PORT, &hints, &list);
    if (rc != 0) {
        fprintf(stderr, "ERROR: cannot resolve host \"%s\" (%s)\n",
                hostname, gai_strerror(rc));
        exit(EXIT_FAILURE);
    }

    for (ai = list; ai != NULL; ai = ai->ai_next) {
        fd = socket(ai->ai_family, ai->ai_socktype, ai->ai_protocol);
        if (fd == -1) {
            last_err = errno;
            continue;
        }

        /* connect in non-blocking mode so we can stop waiting
           after CONNECT_TIMEOUT_MS instead of the system default */
        flags = fcntl(fd, F_GETFL, 0);
        fcntl(fd, F_SETFL, flags | O_NONBLOCK);

        rc = connect(fd, ai->ai_addr, ai->ai_addrlen);
        if (rc == -1 && errno == EINPROGRESS) {
            struct pollfd pfd;
            int so_error = 0;
            socklen_t len = sizeof so_error;

            pfd.fd = fd;
            pfd.events = POLLOUT;
            pfd.revents = 0;

            rc = poll(&pfd, 1, CONNECT_TIMEOUT_MS);
            if (rc == 0) {
                errno = ETIMEDOUT;
                rc = -1;
            } else if (rc > 0) {
                /* socket is writable, check if the connect worked */
                getsockopt(fd, SOL_SOCKET, SO_ERROR, &so_error, &len);
                if (so_error != 0) {
                    errno = so_error;
                    rc = -1;
                } else {
                    rc = 0;
                }
            }
        }

        if (rc == 0) {
            fcntl(fd, F_SETFL, flags);   /* back to blocking mode */
            break;
        }

        last_err = errno;
        close(fd);
        fd = -1;
    }
    freeaddrinfo(list);

    if (fd == -1) {
        fprintf(stderr, "ERROR: cannot connect to %s:%s (%s)\n",
                hostname, SERVER_PORT, strerror(last_err));
        exit(EXIT_FAILURE);
    }

    return fd;
}

/*
 * send_http_get_request()
 * Input  : sockfd   - connected socket
 *          hostname - goes in the Host header
 *          path     - object to fetch, e.g. "/" or "/index.html"
 * Output : none, the GET request is written to the socket
 */
void send_http_get_request(int sockfd, const char *hostname, const char *path)
{
    char req[REQ_SIZE];
    const char *p;
    size_t left;
    ssize_t n;
    int len;

    /* HTTP/1.0: server closes the connection after the reply and does
       not use chunked encoding. Host is still sent for virtual hosts. */
    len = snprintf(req, sizeof req,
                   "GET %s HTTP/1.0\r\n"
                   "Host: %s\r\n"
                   "User-Agent: simple-http-client\r\n"
                   "\r\n",
                   path, hostname);
    if (len < 0 || (size_t)len >= sizeof req) {
        fprintf(stderr, "ERROR: request too large\n");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    p = req;
    left = (size_t)len;
    while (left > 0) {
        n = send(sockfd, p, left, 0);
        if (n == -1) {
            if (errno == EINTR)
                continue;
            fprintf(stderr, "ERROR: send failed (%s)\n", strerror(errno));
            close(sockfd);
            exit(EXIT_FAILURE);
        }
        p += n;
        left -= (size_t)n;
    }

    printf("HTTP GET request sent to %s\n\n", hostname);
    fflush(stdout);
}

/*
 * receive_http_response()
 * Input  : sockfd - connected socket
 * Output : none, the response is printed on stdout
 * Reads until the server closes the connection. poll() is used so the
 * client gives up if the server goes quiet for READ_TIMEOUT_MS.
 */
void receive_http_response(int sockfd)
{
    char chunk[RECV_CHUNK];
    struct pollfd pfd;
    size_t received = 0;
    ssize_t n;
    int rc, closed = 0;

    pfd.fd = sockfd;
    pfd.events = POLLIN;
    pfd.revents = 0;

    for (;;) {
        rc = poll(&pfd, 1, READ_TIMEOUT_MS);
        if (rc == 0) {
            fprintf(stderr, "\nERROR: no data from server for %d seconds\n",
                    READ_TIMEOUT_MS / 1000);
            break;
        }
        if (rc == -1) {
            if (errno == EINTR)
                continue;
            fprintf(stderr, "\nERROR: poll failed (%s)\n", strerror(errno));
            break;
        }

        n = recv(sockfd, chunk, sizeof chunk, 0);
        if (n == 0) {
            closed = 1;   /* server closed the connection, reply is complete */
            break;
        }
        if (n == -1) {
            if (errno == EINTR)
                continue;
            fprintf(stderr, "\nERROR: recv failed (%s)\n", strerror(errno));
            break;
        }

        fwrite(chunk, 1, (size_t)n, stdout);
        received += (size_t)n;
    }

    if (received > 0)
        printf("\n\nTotal bytes received: %zu\n", received);
    else if (closed)
        fprintf(stderr, "ERROR: server closed the connection without a response\n");
    fflush(stdout);
}

/*
 * interact_with_server()
 * Input  : hostname, path
 * Output : none
 * Full exchange: connect -> send GET -> print response -> close.
 */
void interact_with_server(const char *hostname, const char *path)
{
    printf("Interacting with server %s...\n\n", hostname);
    fflush(stdout);

    // Call function to create a socket and connect to the server
    int sockfd = create_socket_and_connect(hostname);

    // Call function to send an HTTP GET request
    send_http_get_request(sockfd, hostname, path);

    // Call function to receive and print the HTTP response
    receive_http_response(sockfd);

    // Call function to close the socket
    close(sockfd);
}

/*
 * main()
 * Input  : argv[1] = hostname or IP (an http:// URL also works)
 *          argv[2] = path (optional, default "/")
 * Output : 0 on success, 1 on bad input
 */
int main(int argc, char *argv[])
{
    char hostname[256];
    char path[1024] = "/";
    const char *target;
    size_t hostlen;
    int rc;

    if (argc != 2 && argc != 3) {
        fprintf(stderr, "Usage  : %s <hostname | IP address> [path]\n", argv[0]);
        fprintf(stderr, "Example: %s 127.0.0.53\n", argv[0]);
        return EXIT_FAILURE;
    }

    /* if the server drops the connection while we are sending,
       report the error instead of being killed by SIGPIPE */
    signal(SIGPIPE, SIG_IGN);

    target = argv[1];
    if (strncmp(target, "http://", 7) == 0) {
        target += 7;
    } else if (strstr(target, "://") != NULL) {
        fprintf(stderr, "ERROR: only http:// is supported\n");
        return EXIT_FAILURE;
    }

    /* split "host/some/path" into host and path */
    hostlen = strcspn(target, "/");
    if (hostlen == 0 || hostlen >= sizeof hostname ||
        strlen(target + hostlen) >= sizeof path) {
        fprintf(stderr, "ERROR: invalid address \"%s\"\n", argv[1]);
        return EXIT_FAILURE;
    }
    sscanf(target, "%255[^/]%1023s", hostname, path);

    if (argc == 3) {
        rc = snprintf(path, sizeof path, "%s%s",
                      argv[2][0] == '/' ? "" : "/", argv[2]);
        if (rc < 0 || (size_t)rc >= sizeof path) {
            fprintf(stderr, "ERROR: path is too long\n");
            return EXIT_FAILURE;
        }
    }

    // Call fuction to interact with the server
    interact_with_server(hostname, path);

    return 0;
}
