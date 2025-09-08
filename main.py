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

def system_setup():
    """
    Initializes all system components
    """

    print("\n Setting up system components")

    lb = LoadBalancer(RoutingAlgo.ROTATING)

    print("Adding servers:")
    initial_servers = [
        Server("primary-1", max_capacity=3, base_response_time=0.4),
        Server("primary-2", max_capacity=4, base_response_time=0.5)
    ]

    for server in initial_servers:
        lb.add_server(server)
    
    # create traffic for burst pattern
    traffic_gen = TrafficGenerator(lb, TrafficPattern.BURST)

    # auto scaler creator
    auto_scaler = AutoScaler(lb, min_servers=2, max_servers=8)

    # make dashboard
    dashboard = Dashboard(lb, traffic_gen, auto_scaler)
    print("System setup is complete")

    return lb, traffic_gen, auto_scaler, dashboard

    


