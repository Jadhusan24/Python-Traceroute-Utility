import socket 
import struct
from .icmp import ping, chksum


def traceroute(dest_host: str, hops: int, timeout: int):
    try:
        # Get the hostname/IP 
        dest_addr = socket.gethostbyname(dest_host)
    except socket.gaierror:
        print("Invalid destination!")
        exit(1)
    print(f"Tracert to {dest_addr} ({dest_host})\nover a maximum of {hops} hops:")
    # Create the ICMP protocol
    icmp_proto = socket.getprotobyname("icmp")
    # Set the initial id and time_to_live values
    time_to_live = 1
    id = 1
    try:
        for hop in range(1, hops+1):
            try:
                # Create the socket
                icmp_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_RAW, icmp_proto)
            except socket.error as e:
                print(f"Error {e}")
                exit(1)
            # increase the ttl and id to the hop number
            time_to_live = hop
            id = hop
            # Ping the host, and if ping is successful then break
            if(ping(dest_addr, icmp_socket, time_to_live, id, timeout)):
                icmp_socket.close()
                break
            # if ping timed out and returned false close socket and restart with a longer ttl and a new id
            icmp_socket.close()
        exit(0)
    except KeyboardInterrupt:
        print("\n[END] EXITING TRACE  ")