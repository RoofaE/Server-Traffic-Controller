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
    
    def route_request(self, request_id):
        """
        Decide which server should handle this reuqest

        This is called everytime a new web request comes in
        """

        with self.lock:
            self.total_requests_routed += 1

            if not self.servers:
                print(f"No servers available for request {request_id}")
                self.failed_requests += 1
                return False
            
            # Choose server based on algo (from enum)
            selected_server = self.select_server()

            if not selected_server:
                print(f"No available servers for request {request_id}")
                self.failed_requests += 1
                return False
            
        # Route the request outside the lock so other requests can start while this is processed
        print(f"Routing request {request_id} to {selected_server.server_id}")

        # Process the request in a different thread so it doesnt block the load balancer
        request_thread = threading.Thread(target=selected_server.process_request, args=(request_id,))
        request_thread.start()

        return True
    
    def _select_server(self):
        """
        Choose which server should handle the next request
        """
        
        if self.rounting_algo == RoutingAlgo.ROTATING:
            return self._select_server_round_robin()
        elif self.rounting_algo == RoutingAlgo.LEAST_CONNECTIONS:
            return self._select_server_least_connections()
        else:
            return self._rotating_selection()
    
    def _rotating_selection(self):
        """
        Cycle through servers in order
        """

        attempts = 0
        startIndex = self.current_server_index

        while attempts < len(self.servers):
            server = self.servers[self.current_server_index]

            # move to next server for next request
            self.current_server_index = (self.current_server_index +1) % len(self.servers) # use startIndex
            attempts += 1

            # check if this server can handle the request
            if server.can_handle_request():
                return server
        
        # no servers available
        return None
    
    
        
        
        
        
        

