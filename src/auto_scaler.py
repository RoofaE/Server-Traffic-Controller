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
        """
        Start the auto scaler monitoring
        """

        self.is_running = True
        threading.Thread(target=self._monitor).start()
        print("Auto Scaler started")
    
    def stop(self):
        """
        Stop the auto scaler
        """
        self.is_running = False
        print("Auto Scaler stopped")
    
    def _monitor(self):
        """
        Check system load and scale up or down as needed
        """
        while self.is_running:
            time.sleep(5) # check every 5 seconds

            # not too often
            if time.time() - self.last_scale_time < 10:
                continue

            stats = self.load_balancer.get_stats()
            util = stats['util']
            server_count = stats['total_servers']

            # scale up if busy
            if util > 70 and server_count < self.max_servers:
                self._add_server()
            
            # scale down if quiet
            elif util < 30 and server_count > self.min_servers:
                self._remove_server()
    
    def _add_server(self):
        pass