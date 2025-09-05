import time
import random
import threading
from enum import Enum
from datetime import datetime

class ServerState(Enum):
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
        self.status = ServerState.HEALTHY
        self.last_request_time = None

        # Thread safety
        self.lock = threading.Lock()

        print(f"Server {self.server_id} initialized with max capacity {self.max_capacity} and base response time {self.base_response_time}s")

    def can_handle_request(self):
        # Can the server take more requests -- checker
        return self.current_requests < self.max_capacity and self.status == ServerState.HEALTHY

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
        
        print(f"Server {self.server_id} complted request {request_id}")
        return True

    
    

    
