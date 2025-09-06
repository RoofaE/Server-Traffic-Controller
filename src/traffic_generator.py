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
    
    def _generate_traffic(self):
        """
        Main traffic generation, this runs on a diff thread
        """
        start_time = time.time()

        while self.is_running:
            # calculates how long were running for (gradual increase pattern)
            elapsed_time = time.time - start_time

            # decides how many requests needed to send based on pattern
            requests_to_send = self._calculate_request_count(elapsed_time)

            # send the requests
            for _ in range(requests_to_send):
                if not self.is_running:
                    break

                self.request_counter +=1
                request_id = f"Traffic-{self.request_counter:04d}" # 4 digit decimal

                # send request to load balancer
                self.load_balancer.route_request(request_id)
            
            # wait before next requests
            sleep_time = self._calculate_sleep_time(elapsed_time)
            time.sleep(sleep_time)
        
        
    def _calculate_sleep_count(self, elapsed_time):
        """
        Decide how many requests to send this time
        """
    
        if self.pattern == TrafficPattern.STEADY:
            # have 1-2 requests for every cycle
            return random.randint(1,2)
        elif self.pattern == TrafficPattern.BURST:
            # quiet with sudden spikes
            if random.random() < 0.1: # 10% chance burst
                print("Traffic Spike Happened")
                return random.randint(5,10) # big burst
            else:
                return random.randint(0, 1) # quiet the rest of the time

        elif self.pattern == TrafficPattern.GRADUAL_INCREASE:
            # start slow, gt busier over time
            base_requests = 1
            growth_factor = elapsed_time/30 # this gts busier every 30secs
            max_requests = int(base_requests + growth_factor)
            return random.randint(1, max(1, max_requests))
        
        elif self.pattern == TrafficPattern.RANDOM:
            return random.randint(0, 5) # unpredictable

        else:
            return 1


    def _calculate_sleep_time(self, elapsed_time):
        """
        Decide how long to wait before next batch of requests
        """

        if self.pattern == TrafficPattern.STEADY:
            return random.uniform(1.0, 2.0) # 102 seconds between batches
        
        elif self.pattern == TrafficPattern.BURST:
            return random.uniform(0.5, 3.0) # more variable and varaible timing
        
        elif self.pattern == TrafficPattern.GRADUAL_INCREASE:
            # when traffic incrases, requests come faster
            base_sleep = 2.0
            speed_factor = elapsed_time / 60 # get faster every minute
            sleep_time = max(0.2, base_sleep - speed_factor) 
            return sleep_time
        
        elif self.pattern == TrafficPattern.RANDOM:
            return random.uniform(0.1, 4.0) # unpredictable timing

        else:
            return 1.0 # default 1 second
        
    def get_stats(self):
        """
        Get traffic generator stats
        """

        return {
            "pattern": self.pattern.value,
            "total_requests_sent": self.request_counter,
            "is_running": self.is_running
        }
    
# Test the traffic generator
if __name__ == "__main__":
    pass
        