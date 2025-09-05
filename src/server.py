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