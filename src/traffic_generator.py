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
        