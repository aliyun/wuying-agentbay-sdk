# Complete Network Operations Guide

This guide provides comprehensive guidance on using network management capabilities in the AgentBay SDK, including network creation, status monitoring, and lifecycle management.

## 📋 Table of Contents

- [Core Concepts](#core-concepts)
- [API Quick Reference](#api-quick-reference)
- [Network Creation](#network-creation)
- [Network Status Monitoring](#network-status-monitoring)
- [Session Integration](#session-integration)
- [Advanced Usage Examples](#advanced-usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

<a id="core-concepts"></a>
## 🎯 Core Concepts

### What is Network Management?

AgentBay's network management functionality allows you to create and manage network configurations for cloud computing environments. This provides:

- **Network Isolation**: Create independent network environments
- **Status Monitoring**: Query network availability and readiness
- **Session Integration**: Associate networks with specific sessions
- **Lifecycle Management**: Control the complete network lifecycle

### Key Components

#### Network ID (NetworkId)
- **Definition**: Unique identifier for a network instance
- **Format**: String typically starting with "net-"
- **Usage**: Required for all network operations after creation

#### Network Token (NetworkToken)
- **Definition**: Security credential for network access
- **Acquisition**: Returned upon successful network creation
- **Purpose**: Used for secure network authentication

#### Online Status
- **Values**: `True` (online) or `False` (offline)
- **Meaning**: Indicates whether the network is ready for use
- **Check Method**: Use `describe_network()` to query current status

<a id="api-quick-reference"></a>
## 🚀 API Quick Reference

### Basic Operations
```python
from agentbay import AgentBay

# Initialize client
agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()
session = session_result.session

# Create network
create_result = session.network.create_network("linux_latest")
if create_result.success:
    network_id = create_result.network_info.network_id
    network_token = create_result.network_info.network_token

# Query network status
describe_result = session.network.describe_network(network_id)
if describe_result.success:
    online_status = describe_result.network_info.online
```

### Session Integration
```python
from agentbay.session_params import CreateSessionParams

# Create session with specific network
params = CreateSessionParams(
    image_id="linux_latest",
    network_id=network_id,
    labels={"purpose": "network_demo"}
)
session_result = agent_bay.create(params)
```

<a id="network-creation"></a>
## 📡 Network Creation

### Basic Network Creation

Create a network with system-generated ID:

```python
from agentbay import AgentBay

# Initialize AgentBay client
agent_bay = AgentBay(api_key=api_key)
session_result = agent_bay.create()

if session_result.success:
    session = session_result.session
    
    # Create network with default settings
    create_result = session.network.create_network("linux_latest")
    
    if create_result.success:
        network_info = create_result.network_info
        print(f"✅ Network created successfully")
        print(f"   Network ID: {network_info.network_id}")
        print(f"   Network Token: {network_info.network_token}")
    else:
        print(f"❌ Network creation failed: {create_result.error_message}")
```

### Custom Network ID Creation

Specify a custom network identifier:

```python
# Create network with custom ID
custom_network_id = "net-my-custom-network"
create_result = session.network.create_network("linux_latest", custom_network_id)

if create_result.success:
    network_info = create_result.network_info
    print(f"✅ Custom network created")
    print(f"   Requested ID: {custom_network_id}")
    print(f"   Actual ID: {network_info.network_id}")
    print(f"   Token: {network_info.network_token}")
else:
    print(f"❌ Custom network creation failed: {create_result.error_message}")
```

### Supported Image Types

Common image identifiers for network creation:

| Image ID | Description | Use Case |
|----------|-------------|----------|
| `linux_latest` | Latest Linux environment | General purpose computing |
| `ubuntu_20.04` | Ubuntu 20.04 LTS | Ubuntu-specific applications |
| `windows_latest` | Latest Windows environment | Windows-specific tasks |

<a id="network-status-monitoring"></a>
## 📊 Network Status Monitoring

### Basic Status Query

Query network details and status:

```python
def check_network_details(session, network_id):
    """Query and display network information"""
    describe_result = session.network.describe_network(network_id)
    
    if describe_result.success:
        network_info = describe_result.network_info
        status = "Online" if network_info.online else "Offline"
        
        print(f"📊 Network Details:")
        print(f"   ID: {network_info.network_id}")
        print(f"   Status: {status}")
        print(f"   Ready: {'Yes' if network_info.online else 'No'}")
        
        return network_info.online
    else:
        print(f"❌ Failed to query network: {describe_result.error_message}")
        return False

# Usage
network_id = "net-123456789"
is_online = check_network_details(session, network_id)
```

### Status Monitoring with Polling

Monitor network status over time:

```python
import time

def wait_for_network_ready(session, network_id, timeout=300, poll_interval=10):
    """Wait for network to become ready"""
    print(f"⏳ Waiting for network {network_id} to come online...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        describe_result = session.network.describe_network(network_id)
        
        if describe_result.success:
            if describe_result.network_info.online:
                elapsed = int(time.time() - start_time)
                print(f"✅ Network is online after {elapsed} seconds")
                return True
            else:
                print(f"⏳ Network still offline, checking again in {poll_interval}s...")
                time.sleep(poll_interval)
        else:
            print(f"❌ Status check failed: {describe_result.error_message}")
            return False
    
    print(f"⏰ Timeout after {timeout} seconds")
    return False

# Usage
network_ready = wait_for_network_ready(session, network_id)
if network_ready:
    print("Network is ready for use")
```

<a id="session-integration"></a>
## 🔗 Session Integration

### Creating Sessions with Specific Networks

Associate a network with a new session:

```python
from agentbay.session_params import CreateSessionParams

def create_session_with_network(agent_bay, network_id):
    """Create a session using a specific network"""
    params = CreateSessionParams(
        image_id="linux_latest",
        network_id=network_id,
        labels={
            "purpose": "network_integration",
            "network_id": network_id
        }
    )
    
    session_result = agent_bay.create(params)
    
    if session_result.success:
        session = session_result.session
        print(f"✅ Session created with network {network_id}")
        print(f"   Session ID: {session.session_id}")
        return session
    else:
        print(f"❌ Session creation failed: {session_result.error_message}")
        return None

# Create network first, then session
create_result = session.network.create_network("linux_latest")
if create_result.success:
    network_id = create_result.network_info.network_id
    new_session = create_session_with_network(agent_bay, network_id)
```

### Network-Aware Session Management

Manage multiple sessions with different networks:

```python
class NetworkSessionManager:
    def __init__(self, agent_bay):
        self.agent_bay = agent_bay
        self.sessions = {}
        self.networks = {}
    
    def create_network_session(self, image_id, network_id=None, labels=None):
        """Create a session with its own network"""
        # First create a session to access network operations
        temp_session_result = self.agent_bay.create()
        if not temp_session_result.success:
            return None, None
        
        temp_session = temp_session_result.session
        
        try:
            # Create network
            create_result = temp_session.network.create_network(image_id, network_id)
            if not create_result.success:
                self.agent_bay.delete(temp_session)
                return None, None
            
            network_info = create_result.network_info
            actual_network_id = network_info.network_id
            
            # Create session with the network
            params = CreateSessionParams(
                image_id=image_id,
                network_id=actual_network_id,
                labels=labels or {}
            )
            
            session_result = self.agent_bay.create(params)
            if session_result.success:
                session = session_result.session
                self.sessions[session.session_id] = session
                self.networks[actual_network_id] = network_info
                
                print(f"✅ Created session {session.session_id} with network {actual_network_id}")
                return session, network_info
            
        finally:
            # Clean up temporary session
            self.agent_bay.delete(temp_session)
        
        return None, None
    
    def cleanup_all(self):
        """Clean up all managed sessions"""
        for session in self.sessions.values():
            try:
                self.agent_bay.delete(session)
            except Exception as e:
                print(f"Warning: Failed to delete session: {e}")
        
        self.sessions.clear()
        self.networks.clear()
        print("✅ All sessions cleaned up")

# Usage
manager = NetworkSessionManager(agent_bay)
session1, network1 = manager.create_network_session("linux_latest")
session2, network2 = manager.create_network_session("ubuntu_20.04")

# Use sessions...
# Clean up when done
manager.cleanup_all()
```

<a id="advanced-usage-examples"></a>
## 🔧 Advanced Usage Examples

### Batch Network Operations

Create and manage multiple networks:

```python
def create_network_pool(session, image_id, count=3, prefix="pool-net"):
    """Create a pool of networks for load balancing"""
    networks = []
    
    print(f"🏗️ Creating {count} networks...")
    
    for i in range(count):
        network_id = f"{prefix}-{i+1:02d}"
        create_result = session.network.create_network(image_id, network_id)
        
        if create_result.success:
            network_info = create_result.network_info
            networks.append({
                'id': network_info.network_id,
                'token': network_info.network_token,
                'index': i + 1,
                'status': 'created'
            })
            print(f"   ✅ Network {i+1}: {network_info.network_id}")
        else:
            print(f"   ❌ Network {i+1} failed: {create_result.error_message}")
    
    print(f"📊 Successfully created {len(networks)}/{count} networks")
    return networks

def check_network_pool_status(session, networks):
    """Check status of all networks in pool"""
    print("🔍 Checking network pool status...")
    
    online_count = 0
    for network in networks:
        describe_result = session.network.describe_network(network['id'])
        
        if describe_result.success:
            online = describe_result.network_info.online
            network['status'] = 'online' if online else 'offline'
            status_icon = '🟢' if online else '🔴'
            print(f"   {status_icon} {network['id']}: {network['status']}")
            
            if online:
                online_count += 1
        else:
            network['status'] = 'error'
            print(f"   ❌ {network['id']}: query failed")
    
    print(f"📈 Pool status: {online_count}/{len(networks)} networks online")
    return online_count, networks

# Create and monitor network pool
networks = create_network_pool(session, "linux_latest", 5)
online_count, updated_networks = check_network_pool_status(session, networks)
```

### Network Health Monitoring

Implement comprehensive network monitoring:

```python
import time
from datetime import datetime, timedelta

class NetworkHealthMonitor:
    def __init__(self, session):
        self.session = session
        self.monitored_networks = {}
        self.health_history = {}
    
    def add_network(self, network_id, check_interval=60):
        """Add a network to monitoring"""
        self.monitored_networks[network_id] = {
            'check_interval': check_interval,
            'last_check': None,
            'status': 'unknown',
            'consecutive_failures': 0
        }
        self.health_history[network_id] = []
        print(f"📊 Added {network_id} to monitoring")
    
    def check_network_health(self, network_id):
        """Check health of a specific network"""
        describe_result = self.session.network.describe_network(network_id)
        
        timestamp = datetime.now()
        
        if describe_result.success:
            online = describe_result.network_info.online
            status = 'healthy' if online else 'offline'
            
            # Update monitoring data
            self.monitored_networks[network_id].update({
                'last_check': timestamp,
                'status': status,
                'consecutive_failures': 0 if online else 
                    self.monitored_networks[network_id]['consecutive_failures'] + 1
            })
            
            # Record health history
            self.health_history[network_id].append({
                'timestamp': timestamp,
                'status': status,
                'online': online
            })
            
            return online
        else:
            # Handle check failure
            self.monitored_networks[network_id].update({
                'last_check': timestamp,
                'status': 'check_failed',
                'consecutive_failures': self.monitored_networks[network_id]['consecutive_failures'] + 1
            })
            
            self.health_history[network_id].append({
                'timestamp': timestamp,
                'status': 'check_failed',
                'online': False,
                'error': describe_result.error_message
            })
            
            return False
    
    def get_health_report(self, network_id, hours=24):
        """Generate health report for a network"""
        if network_id not in self.health_history:
            return None
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_history = [
            record for record in self.health_history[network_id]
            if record['timestamp'] > cutoff_time
        ]
        
        if not recent_history:
            return None
        
        total_checks = len(recent_history)
        healthy_checks = sum(1 for record in recent_history if record.get('online', False))
        uptime_percentage = (healthy_checks / total_checks) * 100
        
        current_status = self.monitored_networks[network_id]['status']
        consecutive_failures = self.monitored_networks[network_id]['consecutive_failures']
        
        return {
            'network_id': network_id,
            'period_hours': hours,
            'total_checks': total_checks,
            'healthy_checks': healthy_checks,
            'uptime_percentage': uptime_percentage,
            'current_status': current_status,
            'consecutive_failures': consecutive_failures,
            'last_check': self.monitored_networks[network_id]['last_check']
        }
    
    def monitor_all(self, duration_minutes=10):
        """Monitor all registered networks for specified duration"""
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        print(f"🔄 Starting monitoring for {duration_minutes} minutes...")
        
        while datetime.now() < end_time:
            for network_id in self.monitored_networks:
                try:
                    is_healthy = self.check_network_health(network_id)
                    status_icon = '🟢' if is_healthy else '🔴'
                    print(f"{status_icon} {network_id}: {'Healthy' if is_healthy else 'Unhealthy'}")
                    
                except Exception as e:
                    print(f"❌ Error checking {network_id}: {e}")
            
            print(f"⏱️ Sleeping for 30 seconds...")
            time.sleep(30)
        
        print("✅ Monitoring completed")

# Usage example
monitor = NetworkHealthMonitor(session)
monitor.add_network("net-123456")
monitor.add_network("net-789012")

# Run monitoring
monitor.monitor_all(duration_minutes=5)

# Get health reports
for network_id in monitor.monitored_networks:
    report = monitor.get_health_report(network_id)
    if report:
        print(f"📊 {network_id} - Uptime: {report['uptime_percentage']:.1f}%")
```

<a id="error-handling"></a>
## ⚠️ Error Handling

### Common Error Scenarios

Handle typical network operation failures:

```python
from agentbay.exceptions import NetworkError, AgentBayError

def robust_network_creation(session, image_id, network_id=None, max_retries=3):
    """Create network with comprehensive error handling"""
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_retries}: Creating network...")
            
            create_result = session.network.create_network(image_id, network_id)
            
            if create_result.success:
                network_info = create_result.network_info
                print(f"✅ Network created: {network_info.network_id}")
                return network_info
            else:
                error_msg = create_result.error_message.lower()
                
                if "image not found" in error_msg:
                    print(f"❌ Invalid image ID: {image_id}")
                    break  # Don't retry for invalid image
                elif "quota exceeded" in error_msg:
                    print(f"⚠️ Quota exceeded, retrying in 30 seconds...")
                    time.sleep(30)
                elif "network id already exists" in error_msg:
                    print(f"❌ Network ID {network_id} already exists")
                    break  # Don't retry for duplicate ID
                else:
                    print(f"❌ Creation failed: {create_result.error_message}")
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        print(f"⏳ Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                
        except NetworkError as e:
            print(f"❌ Network error: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
        except AgentBayError as e:
            print(f"❌ AgentBay error: {e}")
            break  # Don't retry for general AgentBay errors
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    
    print(f"❌ Failed to create network after {max_retries} attempts")
    return None

def safe_network_query(session, network_id):
    """Query network with error handling"""
    try:
        describe_result = session.network.describe_network(network_id)
        
        if describe_result.success:
            return describe_result.network_info
        else:
            error_msg = describe_result.error_message.lower()
            
            if "not found" in error_msg:
                print(f"❌ Network {network_id} does not exist")
            elif "permission denied" in error_msg:
                print(f"❌ Insufficient permissions for network {network_id}")
            else:
                print(f"❌ Query failed: {describe_result.error_message}")
            
            return None
            
    except Exception as e:
        print(f"❌ Query error: {e}")
        return None

# Usage
network_info = robust_network_creation(session, "linux_latest")
if network_info:
    query_result = safe_network_query(session, network_info.network_id)
```

### Error Recovery Patterns

Implement recovery strategies for common failures:

```python
def network_operation_with_recovery(session, operation_func, *args, **kwargs):
    """Execute network operation with automatic recovery"""
    max_attempts = 3
    backoff_delay = 1
    
    for attempt in range(max_attempts):
        try:
            result = operation_func(session, *args, **kwargs)
            
            if hasattr(result, 'success') and result.success:
                return result
            elif hasattr(result, 'error_message'):
                print(f"⚠️ Operation failed: {result.error_message}")
                
                # Check if retry is worthwhile
                if "temporary" in result.error_message.lower() or \
                   "busy" in result.error_message.lower():
                    if attempt < max_attempts - 1:
                        print(f"🔄 Retrying in {backoff_delay} seconds...")
                        time.sleep(backoff_delay)
                        backoff_delay *= 2  # Exponential backoff
                        continue
                
                return result
            else:
                return result
                
        except Exception as e:
            print(f"❌ Exception on attempt {attempt + 1}: {e}")
            if attempt < max_attempts - 1:
                time.sleep(backoff_delay)
                backoff_delay *= 2
    
    print(f"❌ Operation failed after {max_attempts} attempts")
    return None

# Usage
def create_network_operation(session, image_id, network_id=None):
    return session.network.create_network(image_id, network_id)

result = network_operation_with_recovery(session, create_network_operation, "linux_latest")
```

<a id="best-practices"></a>
## 💡 Best Practices

### 1. Network Lifecycle Management

Implement proper lifecycle management:

```python
class NetworkLifecycleManager:
    def __init__(self, session):
        self.session = session
        self.managed_networks = []
        self.creation_metadata = {}
    
    def create_managed_network(self, image_id, network_id=None, metadata=None):
        """Create and track network with metadata"""
        create_result = self.session.network.create_network(image_id, network_id)
        
        if create_result.success:
            network_info = create_result.network_info
            actual_network_id = network_info.network_id
            
            # Track the network
            self.managed_networks.append(actual_network_id)
            
            # Store metadata
            self.creation_metadata[actual_network_id] = {
                'created_at': datetime.now(),
                'image_id': image_id,
                'requested_id': network_id,
                'custom_metadata': metadata or {}
            }
            
            print(f"✅ Created and tracking network: {actual_network_id}")
            return network_info
        else:
            print(f"❌ Network creation failed: {create_result.error_message}")
            return None
    
    def get_network_metadata(self, network_id):
        """Get stored metadata for a network"""
        return self.creation_metadata.get(network_id)
    
    def list_managed_networks(self):
        """List all managed networks with their status"""
        print(f"📋 Managed Networks ({len(self.managed_networks)}):")
        
        for network_id in self.managed_networks:
            metadata = self.creation_metadata.get(network_id, {})
            created_at = metadata.get('created_at', 'Unknown')
            
            # Check current status
            describe_result = self.session.network.describe_network(network_id)
            if describe_result.success:
                status = 'Online' if describe_result.network_info.online else 'Offline'
                status_icon = '🟢' if describe_result.network_info.online else '🔴'
            else:
                status = 'Query Failed'
                status_icon = '❌'
            
            print(f"   {status_icon} {network_id}")
            print(f"      Status: {status}")
            print(f"      Created: {created_at}")
            print(f"      Image: {metadata.get('image_id', 'Unknown')}")
    
    def cleanup_all(self):
        """Clean up tracking (networks persist in cloud)"""
        print(f"🧹 Cleaning up tracking for {len(self.managed_networks)} networks")
        self.managed_networks.clear()
        self.creation_metadata.clear()
        print("✅ Tracking cleanup completed")

# Usage
lifecycle_mgr = NetworkLifecycleManager(session)

# Create networks with metadata
net1 = lifecycle_mgr.create_managed_network(
    "linux_latest", 
    metadata={"purpose": "development", "team": "backend"}
)

net2 = lifecycle_mgr.create_managed_network(
    "ubuntu_20.04",
    metadata={"purpose": "testing", "team": "qa"}
)

# List managed networks
lifecycle_mgr.list_managed_networks()

# Cleanup tracking when done
lifecycle_mgr.cleanup_all()
```

### 2. Performance Optimization

Optimize network operations for better performance:

```python
import concurrent.futures
from threading import Lock

class OptimizedNetworkManager:
    def __init__(self, session, max_workers=5):
        self.session = session
        self.max_workers = max_workers
        self.results_lock = Lock()
        self.results = {}
    
    def create_networks_parallel(self, network_configs):
        """Create multiple networks in parallel"""
        print(f"🚀 Creating {len(network_configs)} networks in parallel...")
        
        def create_single_network(config):
            network_id = config.get('network_id')
            image_id = config.get('image_id', 'linux_latest')
            
            try:
                create_result = self.session.network.create_network(image_id, network_id)
                
                with self.results_lock:
                    self.results[network_id or f"auto-{id(config)}"] = {
                        'success': create_result.success,
                        'network_info': create_result.network_info if create_result.success else None,
                        'error': create_result.error_message if not create_result.success else None
                    }
                
                return create_result.success
                
            except Exception as e:
                with self.results_lock:
                    self.results[network_id or f"auto-{id(config)}"] = {
                        'success': False,
                        'network_info': None,
                        'error': str(e)
                    }
                return False
        
        # Execute in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(create_single_network, config): config 
                for config in network_configs
            }
            
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                success = future.result()
                completed += 1
                status = "✅" if success else "❌"
                print(f"   {status} Network {completed}/{len(network_configs)} completed")
        
        # Summary
        successful = sum(1 for r in self.results.values() if r['success'])
        print(f"📊 Parallel creation completed: {successful}/{len(network_configs)} successful")
        
        return self.results
    
    def check_networks_parallel(self, network_ids):
        """Check multiple network statuses in parallel"""
        print(f"🔍 Checking {len(network_ids)} networks in parallel...")
        
        status_results = {}
        status_lock = Lock()
        
        def check_single_network(network_id):
            try:
                describe_result = self.session.network.describe_network(network_id)
                
                with status_lock:
                    if describe_result.success:
                        status_results[network_id] = {
                            'online': describe_result.network_info.online,
                            'error': None
                        }
                    else:
                        status_results[network_id] = {
                            'online': False,
                            'error': describe_result.error_message
                        }
                
                return describe_result.success
                
            except Exception as e:
                with status_lock:
                    status_results[network_id] = {
                        'online': False,
                        'error': str(e)
                    }
                return False
        
        # Execute parallel checks
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(check_single_network, network_id): network_id 
                for network_id in network_ids
            }
            
            for future in concurrent.futures.as_completed(futures):
                network_id = futures[future]
                success = future.result()
                
                if success and status_results[network_id]['online']:
                    print(f"   🟢 {network_id}: Online")
                elif success:
                    print(f"   🔴 {network_id}: Offline")
                else:
                    print(f"   ❌ {network_id}: Check failed")
        
        online_count = sum(1 for r in status_results.values() if r['online'])
        print(f"📊 Status check completed: {online_count}/{len(network_ids)} networks online")
        
        return status_results

# Usage example
optimizer = OptimizedNetworkManager(session, max_workers=3)

# Create multiple networks in parallel
network_configs = [
    {'image_id': 'linux_latest', 'network_id': 'net-parallel-1'},
    {'image_id': 'ubuntu_20.04', 'network_id': 'net-parallel-2'},
    {'image_id': 'linux_latest', 'network_id': 'net-parallel-3'},
]

creation_results = optimizer.create_networks_parallel(network_configs)

# Extract successful network IDs
successful_networks = [
    result['network_info'].network_id 
    for result in creation_results.values() 
    if result['success'] and result['network_info']
]

# Check their status in parallel
if successful_networks:
    status_results = optimizer.check_networks_parallel(successful_networks)
```

### 3. Resource Management

Implement proper resource management patterns:

```python
from contextlib import contextmanager

@contextmanager
def managed_network_session(agent_bay, image_id, network_id=None):
    """Context manager for network and session lifecycle"""
    temp_session = None
    main_session = None
    network_info = None
    
    try:
        # Create temporary session for network creation
        temp_result = agent_bay.create()
        if not temp_result.success:
            raise Exception(f"Failed to create temporary session: {temp_result.error_message}")
        
        temp_session = temp_result.session
        
        # Create network
        create_result = temp_session.network.create_network(image_id, network_id)
        if not create_result.success:
            raise Exception(f"Failed to create network: {create_result.error_message}")
        
        network_info = create_result.network_info
        print(f"✅ Network created: {network_info.network_id}")
        
        # Create main session with the network
        from agentbay.session_params import CreateSessionParams
        params = CreateSessionParams(
            image_id=image_id,
            network_id=network_info.network_id
        )
        
        main_result = agent_bay.create(params)
        if not main_result.success:
            raise Exception(f"Failed to create main session: {main_result.error_message}")
        
        main_session = main_result.session
        print(f"✅ Session created: {main_session.session_id}")
        
        # Yield the session and network info for use
        yield main_session, network_info
        
    except Exception as e:
        print(f"❌ Error in managed network session: {e}")
        raise
    
    finally:
        # Cleanup in reverse order
        if main_session:
            try:
                agent_bay.delete(main_session)
                print(f"✅ Main session cleaned up")
            except Exception as e:
                print(f"⚠️ Failed to cleanup main session: {e}")
        
        if temp_session:
            try:
                agent_bay.delete(temp_session)
                print(f"✅ Temporary session cleaned up")
            except Exception as e:
                print(f"⚠️ Failed to cleanup temporary session: {e}")
        
        if network_info:
            print(f"ℹ️ Network {network_info.network_id} remains in cloud")

# Usage with automatic cleanup
try:
    with managed_network_session(agent_bay, "linux_latest") as (session, network):
        print(f"Using session {session.session_id} with network {network.network_id}")
        
        # Perform operations...
        result = session.command.execute_command("echo 'Hello from networked session'")
        print(f"Command result: {result.output}")
        
        # Any exception here will trigger cleanup
        
except Exception as e:
    print(f"❌ Operation failed: {e}")

print("✅ All resources cleaned up automatically")
```

---

This comprehensive guide covers all aspects of network operations in the AgentBay SDK. For additional information, refer to the [API Reference Documentation](../python/docs/api/network.md) and [Network Management Examples](../python/docs/examples/network_management/).