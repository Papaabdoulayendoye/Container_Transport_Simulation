from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid

@dataclass
class Terminal:
    id: str
    name: str
    capacity: int  # Maximum number of containers that can be stored
    current_containers: int = 0

@dataclass
class Container:
    id: str
    type: str  # Container type (standardized to TEU)
    origin: str  # Terminal ID
    destination: str  # Terminal ID
    request_date: datetime
    available_date: datetime
    due_date: datetime
    priority: int
    status: str = "waiting"  # waiting, in_transit, delivered

@dataclass
class Service:
    id: str
    origin: str  # Terminal ID
    destination: str  # Terminal ID
    capacity: int  # Maximum number of containers
    duration: timedelta
    schedule: List[datetime]  # List of departure times
    current_load: int = 0

@dataclass
class Barge:
    id: str
    capacity: int
    current_terminal: Optional[str] = None  # Terminal ID
    current_service: Optional[str] = None  # Service ID
    containers: List[str] = None  # List of container IDs
    status: str = "idle"  # idle, loading, in_transit, unloading, maintenance

    def __post_init__(self):
        if self.containers is None:
            self.containers = []

class TransportSimulation:
    def __init__(self):
        self.terminals: Dict[str, Terminal] = {}
        self.services: Dict[str, Service] = {}
        self.barges: Dict[str, Barge] = {}
        self.containers: Dict[str, Container] = {}
        self.current_time: datetime = datetime.now()
        
    def add_terminal(self, name: str, capacity: int) -> str:
        terminal_id = str(uuid.uuid4())
        self.terminals[terminal_id] = Terminal(
            id=terminal_id,
            name=name,
            capacity=capacity
        )
        return terminal_id
    
    def add_service(self, origin: str, destination: str, capacity: int,
                   duration: timedelta, schedule: List[datetime]) -> str:
        service_id = str(uuid.uuid4())
        self.services[service_id] = Service(
            id=service_id,
            origin=origin,
            destination=destination,
            capacity=capacity,
            duration=duration,
            schedule=schedule
        )
        return service_id
    
    def add_barge(self, capacity: int, terminal_id: Optional[str] = None) -> str:
        barge_id = str(uuid.uuid4())
        self.barges[barge_id] = Barge(
            id=barge_id,
            capacity=capacity,
            current_terminal=terminal_id
        )
        return barge_id
    
    def add_container_request(self, type: str, origin: str, destination: str,
                            available_date: datetime, due_date: datetime,
                            priority: int) -> str:
        container_id = str(uuid.uuid4())
        self.containers[container_id] = Container(
            id=container_id,
            type=type,
            origin=origin,
            destination=destination,
            request_date=datetime.now(),
            available_date=available_date,
            due_date=due_date,
            priority=priority
        )
        return container_id
    
    def step(self):
        """Advance simulation by one time step"""
        # Update positions and status of all barges
        for barge in self.barges.values():
            if barge.status == "in_transit":
                self._update_barge_position(barge)
            elif barge.status == "idle":
                self._assign_barge_to_service(barge)
                
        # Update container statuses
        self._update_container_statuses()
        
        # Advance time
        self.current_time += timedelta(minutes=1)
    
    def _update_barge_position(self, barge: Barge):
        """Update the position of a barge in transit"""
        # Implementation details to be added
        pass
    
    def _assign_barge_to_service(self, barge: Barge):
        """Try to assign an idle barge to a service"""
        # Implementation details to be added
        pass
    
    def _update_container_statuses(self):
        """Update the status of all containers"""
        # Implementation details to be added
        pass
    
    def get_performance_metrics(self) -> Dict:
        """Calculate and return performance metrics"""
        metrics = {
            "total_containers": len(self.containers),
            "containers_delivered": len([c for c in self.containers.values() if c.status == "delivered"]),
            "active_barges": len([b for b in self.barges.values() if b.status != "idle"]),
            "terminal_utilization": {
                t.name: (t.current_containers / t.capacity) for t in self.terminals.values()
            }
        }
        return metrics
