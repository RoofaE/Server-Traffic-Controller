import threading
import time
from datetime import datetime
from enum import Enum
from server import Server, ServerStatus

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
            self.total_requests += 1

            if not self.servers:
                print(f"No servers available for request {request_id}")
                self.failed_requests += 1
                return False
            
            # Choose server based on algo (from enum)
            selected_server = self._select_server()

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
            return self._rotating_selection()
        elif self.rounting_algo == RoutingAlgo.LEAST_CONNECTIONS:
            return self._least_connections_selection()
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
    
    def _least_connections_selection(self):
        """
        Choose the server with fewest actinve connections
        """

        available_servers = [s for s in self.servers if s.can_handle_request()]

        if not available_servers:
            return None
        
        # Find the server with least current requests
        best_server = min(available_servers, key=lambda s: s.current_requests)
        return best_server
    
    def get_stats(self):
        """
        Get current load balancer stats
        """

        with self.lock:
            healthy_servers = 0
            for s in self.servers:
                if s.status == ServerStatus.HEALTHY:
                    healthy_servers += 1
            
            total_capacity = 0
            for s in self.servers:
                total_capacity += s.max_capacity

            current_load = 0
            for s in self.servers:
                current_load += s.current_requests
        
            return {
                "total_servers": len(self.servers),
                "healthy_servers": healthy_servers,
                "total_requests_routed": self.total_requests,
                "failed_requests": self.failed_requests,
                "success_rate": ((self.total_requests - self.failed_requests) / max(1, self.total_requests)) * 100,
                "total_capacity": total_capacity,
                "current_load": current_load,
                "util": (current_load / max(1, total_capacity)) * 100
            }
        
    def print_stats(self):
        """
        Prints current status of load balancer and all servers
        """
        stats = self.get_stats()

        print("\n--- Load Balancer Stats ---")
        print(f"\n Load Balancer Status:")
        print(f" Algorithm: {self.rounting_algo.value}")
        print(f" Servers: {stats['healthy_servers']}/{stats['total_servers']} healthy")
        print(f" Requests: {stats['total_requests_routed']} total, {stats['failed_requests']} failed")
        print(f" Success Rate: {stats['success_rate']:.1f}%")
        print(f" System Load: {stats['current_load']}/{stats['total_capacity']} ({stats['util']:.1f}%)")
        
        print(f"\n Server Details:")
        for server in self.servers:
            print(f"   {server}")
        print("---------------------------\n")

# Test the load balancer
if __name__ == "__main__":
    # Create load balancer
    lb = LoadBalancer(rounting_algo=RoutingAlgo.ROTATING)

    # Add servers to the pool for testing
    server1 = Server("Server 1", max_capacity=3, base_response_time=0.3)
    server2 = Server("Server 2", max_capacity=5, base_response_time=0.5)
    server3 = Server("Server 3", max_capacity=2, base_response_time=0.2)

    lb.add_server(server1)
    lb.add_server(server2)
    lb.add_server(server3)

    # Initial status
    lb.print_stats()

    # Route some requests
    print(f"\n Routing test requests...")
    for i in range(6):
        request_id = f"req-{i+1:03d}" # start from 1, format string as int with 3 digits
        lb.route_request(request_id)
        time.sleep(0.1)  # Small delay between requests

    # Wait a little bit for requests to process
    time.sleep(3)

    # Show final stats
    lb.print_stats()

