import argparse
from Packages.main import traceroute

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # create arguements
    parser.add_argument('destination_server')
    parser.add_argument('-t', '--timeout', required=False, nargs='?',default=5, type=int, metavar='Timeout in secondsd')
    parser.add_argument('-m', '--maxhops', required=False,nargs='?', default=30, type=int, metavar='Max hops')

    args = parser.parse_args()
    # destruct the args passed
    destination_server, timeout, max_hops = args.destination_server, args.timeout, args.maxhops
    # begin trace
    traceroute(destination_server, max_hops, timeout)
