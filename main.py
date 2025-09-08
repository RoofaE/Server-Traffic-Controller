# all imports including from src file
import time
import sys
from datetime import datetime
from src.load_balancer import LoadBalancer, RoutingAlgo
from src.traffic_generator import TrafficGenerator, TrafficPattern
from src.auto_scaler import AutoScaler
from src.dashboard import Dashboard
from src.server import Server

def welcome():
    """
    Simple display of the project
    """

    print("=============================================================================================")

    print("Server Traffic Controller")
    print("Live Distributed Load Balancer Simulator")
    print("=============================================================================================")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n\n Features Include:")
    print("-> Dynamic traffic routing with ROTATING algo")
    print("-> Real time auto scaling based on the metrics")
    print("-> Concurrent request processing")
    print("-> Live dashboard")
    
    print("=============================================================================================")



