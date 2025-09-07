import time
import threading
import random
from server import Server
from datetime import datetime

class AutoScaler:
    def __init__(self, load_balancer, min_servers=2, max_servers=8):
        """
        Automatically add or remove servers based on the systems load

        Arguments:
            load_balancer: The LoadBalancer instance to manage
            min_servers: Minimum number of servers, never go below this
            max_servers: Maximum number of servers, never go above this
        """

        self.load_balancer = load_balancer
        self.min_servers = min_servers
        self.max_servers = max_servers
        self.server_count = 0
        self.is_running = False
        self.last_scale_time = 0


        print(f"Auto Scaler initialized witn min {min_servers} and max {max_servers} servers")

    
    def start(self):
        pass