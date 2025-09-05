import threading
import time
from datetime import datetime
from enum import Enum
from .server import Server, ServerState

class RoutingAlgo(Enum):
    ROTATING = "rotating"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"


class LoadBalancer:
    def __init__(self, rounting_algo=RoutingAlgo.ROTATING):
        """
        Main Load Balancer class that manages different servers

        Arguments:
            rounting_algo: How to decide which server gets each request
        """

        self.rounting_algo = rounting_algo
        self.servers = []
        self.current_server_index = 0  # For round robin
        self.total_requests = 0
        self.failed_requests = 0

        # Thread safety
        self.lock = threading.Lock()
        print(f"Load Balancer initialized with {rounting_algo.value} algorithm")

    def add_server(self, server):
        """
        Add new server to the pool
        """
        with self.lock:
            self.servers.append(server)
            print(f"Added {server.server_id} to Load Balancer. Total servers: {len(self.servers)}")
    
    def remove_server(self, server_id):
        """
        Remove server from the pool
        """
        with self.lock:
            for i, server in enumerate(self.servers):
                if server.server_id == server_id:
                    removed_server = self.servers.pop(i)
                    print(f"Removed {server_id} from load balancer. Total Servers: {len(self.servers)}")
                    return removed_server
            return None
    
    def route_request(self, server_id):
        """
        Decide which server should handle this reuqest

        This is called everytime a new web request comes in
        """

        