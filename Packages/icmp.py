import socket
import struct
import time

def chksum(header):
    checksum = 0
    overflow = 0
    # For every word (16-bits)
    for i in range(0, len(header), 2):
        word = header[i] + (header[i+1] << 8)
        # Add the current word to the checksum
        checksum = checksum + word
        # Separate the overflow
        overflow = checksum >> 16
        # While there is an overflow
        while overflow > 0:
            # Remove the overflow bits
            checksum = checksum & 0xFFFF
            # Add the overflow bits
            checksum = checksum + overflow
            # Calculate the overflow again
            overflow = checksum >> 16
    # There's always a chance that after calculating the checksum
    # across the header, ther is *still* an overflow, so need to
    # check for that
    overflow = checksum >> 16
    while overflow > 0:
        checksum = checksum & 0xFFFF
        checksum = checksum + overflow
        overflow = checksum >> 16
    # Ones-compliment and return
    checksum = ~checksum
    checksum = checksum & 0xFFFF
    return checksum

# Send ICMP Ping Packet
def ping(dest_addr: str, icmp_socket: socket, time_to_live: int, id: int, timeout: int):
    try:
        # Set initial checksum to zero and create the array
        print(f"{time_to_live}\t ", end="")
        initial_checksum = 0
        initial_header = struct.pack(
            "bbHHh", 8, 0, initial_checksum, id, 1)
        # Calculate the actual checksum and the actual array
        calculated_checksum = chksum(initial_header)
        header = struct.pack("bbHHh", 8,
                             0, calculated_checksum, id, 1)
        # Set the TTL field in the IP section of packet
        icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, time_to_live)
        # Send the packet
        icmp_socket.sendto(header, (dest_addr, 1))
        # Get the time so we can calculate time for response
        start_time = time.time()
        # Wait for response on socket, or timeout after TIMEOUT seconds
        icmp_socket.settimeout(timeout)
        # Read the data from the socket
        recv_packet, addr = icmp_socket.recvfrom(1024)
        hostname = ''
        try:
            # Try and convert the IP to a hostname
            host_details = socket.gethostbyaddr(addr[0])
            if len(host_details) > 0:
                hostname = host_details[0]
        except Exception:
            # if we can't find the hostname, just display 'unknown'
            hostname = 'unknown'
        # Display the time taken to get a response, the ip, and the hostname
        ms = int((time.time() - start_time) * 1000.00)
        print(f'{ms}ms\t{hostname} [{addr[0]}]')
        # If the packet we received back is from the final-destinaton host,
        # then its done!
        if addr[0] == dest_addr:
            return True
        # ..in all other cases, return False
    except socket.timeout as identifier:
        ms = int((time.time() - start_time) * 1000.0)
        print('*\tRequest timed out.')
        return False
    return False