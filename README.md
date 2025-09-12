# Server Traffic Controller

A smart load balancer that automatically routes web traffic across multiple servers and scales up/down based on demand.

## Features:

- **Smart Traffic Routing** - Distributes requests evenly across servers
- **Auto-Scaling** - Adds servers when busy, removes when quiet
- **Traffic Simulation** - Creates realistic traffic patterns with spikes
- **Live Dashboard** - Real time stats and monitoring
- **Concurrent Processing** - Handles multiple requests simultaneously

## Quick Start:

On Windows:
```bash
git clone https://github.com/RoofaE/Server-Traffic-Controller.git
cd server-traffic-controller
python main.py
```
On macOS:
```bash
git clone https://github.com/RoofaE/Server-Traffic-Controller.git
cd server-traffic-controller
python3 main.py
```

This starts everything:
- 2 initial servers
- Traffic generator (creates bursts)
- Auto-scaler (adds/removes servers)
- Live dashboard (shows real-time stats)
  
Watch servers automatically scale up during traffic spikes. 
Press `Ctrl+C` to stop the program

## Testing Individual Parts:

```bash
# Test basic server
python src/server.py

# Test load balancer
python src/load_balancer.py

# Test traffic generator
python src/traffic_generator.py

# Test auto-scaler
python src/auto_scaler.py

# Test dashboard
python src/dashboard.py
```

## Configuration:

- **Min Servers**: 2
- **Max Servers**: 8
- **Scale Up**: When servers > 70% busy
- **Scale Down**: When servers < 30% busy
- **Server Capacity**: 2 to 5 requests each

## Traffic Patterns:

- **STEADY** - Consistent traffic
- **BURST** - Quiet then sudden spikes
- **GRADUAL_INCREASE** - Slowly gets busier
- **RANDOM** - Unpredictable chaos

## Sample Output:
```
Traffic Spike Happened
Routing request Traffic-0038 to primary-2
Routing request Traffic-0039 to primary-1
Routing request Traffic-0040 to primary-2
Routing request Traffic-0041 to primary-1
Routing request Traffic-0042 to primary-2
Routing request Traffic-0043 to primary-1
No available servers for request Traffic-0044
No available servers for request Traffic-0045

>>>>> Scaled UP: Added server Auto-1 (Total: 3)<<<<<

=============================================================================================
LOAD BALANCER: 
 Algorithm: rotating
 Servers: 3 active
 Success Rate: 93.6%
 System Load: 0/10 (0.0%)

 Servers:
 1. primary-1: 0/3 (0%) OFFLINE ○
 2. primary-2: 0/4 (0%) OFFLINE ○
 3. Auto-1: 0/3 (0%) OFFLINE ○

>>>>> Scaled DOWN: Removed server primary-1 (Total: 2)<<<<<
```

## Tech Used 💻

- Python
- Threading (for concurrent requests)
- Real time monitoring
- Auto scaling algorithms



