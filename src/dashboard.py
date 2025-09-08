import time
from datetime import datetime

class Dashboard:
    def __init__(self, load_balancer, traffic_generator=None, auto_scaler=None):
        """
        Dashboard to show real time monitoring of the system

        Arguments:
            load_balancer: Instance of load balancer to monitor
            traffic_generator: TrafficGenerator instance
            auto_scaler: AutoScaler instance
        """

        self.load_balancer = load_balancer
        self.traffic_generator = traffic_generator
        self.auto_scaler = auto_scaler
    
    def display_stats(self):
        """
        Display current system stats
        """

        print("\033[2J\033[H") # this clears terminals whole screen and moves cursor to top left

        print("=============================================================================================")
        print(f"Server Traffic Controller - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=============================================================================================")


        # Load Balancer Stats
        lb_stats = self.load_balancer.get_stats()
        print(f"\nLOAD BALANCER: ")
        print(f" Algorithm: {self.load_balancer.rounting_algo.value}")
        print(f" Servers: {lb_stats["total_servers"]} active")
        print(f" Success Rate: {lb_stats["success_rate"]:.1f}%")
        print(f" System Load: {lb_stats["current_load"]}/{lb_stats["total_capacity"]} ({lb_stats["util"]:.1f}%)")


        # Server details
        print(f"\n Servers:")
        for i, server in enumerate(self.load_balancer.servers, 1):
            stats = server.get_stats()
            status_icon = "ONLINE ●" if stats["status"] == "healthy" else "OFFLINE ○"
            print(f" {i}. {server.server_id}: {stats["current_requests"]}/{server.max_capacity} ({stats["util"]:.0f}%) {status_icon}")
