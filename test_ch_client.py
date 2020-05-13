import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT
from consistent_hashing import consistent_hashing
BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)    
        self.cached_length = 0   

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            self.cached_length += 1
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


def process(udp_clients):

    client_ring = consistent_hashing(udp_clients)
    client_ring.generate_node_ring()
    # PUT all users.
    for u in USERS[0:40]:
        data_bytes, key = serialize_PUT(u)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)
        
    for node in udp_clients:
        print('server at {}:{} cached {} data'.format(node.host, node.port, node.cached_length))
    print("*********************************DELETE NODE 2 FOR REPLICATION TESTING****************************************")
    print("*********************************DELETE NODE 2 FOR REPLICATION TESTING****************************************")
    print("*********************************DELETE NODE 2 FOR REPLICATION TESTING****************************************")
    # testing replication
    client_ring.delete_node(udp_clients[2])
    for u in USERS[41:]:
        data_bytes, key = serialize_PUT(u)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)

    for node in udp_clients:
        print('server at {}:{} cached {} data'.format(node.host, node.port, node.cached_length))    

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)