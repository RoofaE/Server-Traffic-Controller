import time
import threading
import random
from datetime import datetime
from enum import Enum

class TrafficPattern(Enum):
    STEADY = "steady", # consistent traffic
    BURST = "burst", # sudden SPIKE
    GRADUAL_INCREASE = "gradual_increase", # slowly getting busy
    RANDOM = "random" # unpredicted

class TrafficGenerator:
    def __init__(self, load_balancer, pattern=TrafficPattern.STEADY):
        """
        Generates realistic web traffic and sends it to the load balancer

        Arguments:
            load_balancer: LoadBalancer instance to send requests to
            pattern: Which kind of traffic pattern to simulate
        """
        self.load_balancer = load_balancer
        self.pattern = pattern
        self.request_counter = 0
        self.is_running = False
        self.generator_thread = None

        print(f"Traffic Generator createdwith {pattern.value} pattern")
    
    def start(self):
        """
        Start generating the traffic
        """
        if self.is_running:
            print("Traffic Generator is running")
            return

        self.is_running = True
        self.generator_thread = threading.Thread(target=self._generate_traffic)
        self.generator_thread.start()

        print("Traffic Generation has started")

    
    def stop(self):
        """
        Stop generating the traffic
        """
        self.is_running = False
        if self.generator_thread:
            self.generator_thread.join()
        print("Traffic Generation stopped")
    

