import time
import random
import threading
from enum import Enum
from datetime import datetime

class ServerStatus(Enum):
    HEALTHY = "Healthy"
    OVERLOADED = "Overloaded"
    DOWN = "Down"

class Server:
    def __init__(self, server_id, max_capacity=10, base_response_time=0.1):
        """
        Web server simulation

        Arguments:
        server_id : unique identifier for the server
        max_capacity: Max concurrent reqs the server can handle
        base_response_time: In seconds, how long the server takes to process a request
        """
        self.server_id = server_id
        self.max_capacity = max_capacity
        self.base_response_time = base_response_time

        # Current state
        self.current_requests = 0
        self.total_requests_handled = 0
        self.status = ServerStatus.HEALTHY
        self.last_request_time = None

        # Thread safety
        self.lock = threading.Lock()

        print(f"Server {self.server_id} initialized with max capacity {self.max_capacity} and base response time {self.base_response_time}s")

    def can_handle_request(self):
        # Can the server take more requests -- checker
        return self.current_requests < self.max_capacity and self.status == ServerStatus.HEALTHY

    def process_request(self, request_id):
        """
        Simulate processing web request

        Runs by its own thread for concurrency processing
        """

        with self.lock:
            if not self.can_handle_request():
                return False # server full or down
            
            self.current_requests += 1
            self.total_requests_handled += 1
            self.last_request_time = datetime.now()
        
        processing_time = self.calculate_response_time()
        print(f"Server {self.server_id} processing request {request_id} (will take {processing_time:.2f}s)")

        # Show that work is being done
        time.sleep(processing_time)

        # Request done
        with self.lock:
            self.current_requests -= 1
        
        print(f"Server {self.server_id} completed request {request_id}")
        return True

    def calculate_response_time(self):
        """
        Calculates response time on current load
        """
        load_factor = self.current_requests / self.max_capacity

        # When server is busy, response time decreases
        response_time = self.base_response_time * (1 + load_factor)

        return response_time
    
    def get_stats(self):
        """
        Gets the current server stats
        """

        with self.lock:
            util = (self.current_requests / self.max_capacity) * 100

            # update status based on load
            if util > 90:
                self.status = ServerStatus.OVERLOADED
            elif util < 70:
                self.status = ServerStatus.HEALTHY
            
            return {
                "server_id": self.server_id,
                "current_requests": self.current_requests,
                "total_handled": self.total_requests_handled,
                "util": util,
                "status": self.status.value,
                "last_request": self.last_request_time
            }
        
    def __str__(self):
        stats = self.get_stats()
        return f"Server {self.server_id}: {stats['current_requests']}/{self.max_capacity} ({stats['util']:.1f}% - {stats['status']})"
    

if __name__ == "__main__":
    # Server Test
    server = Server("Test 1", max_capacity=3, base_response_time=0.5)

    print(f"Server stats: {server}")
    print(f"Can handle request? {server.can_handle_request()}")

    # Processing a Request Test
    result = server.process_request("Req-1")
    print(f"Request processed: {result}")
    print(f"Server stats: {server}")
