from datetime import datetime, timedelta
from typing import Dict, List
import uuid

from .terminal import Terminal
from .container import Container
from .service import Service
from .barge import Barge

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
    
    def add_barge(self, capacity: int, terminal_id: str = None) -> str:
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
        self.current_time += timedelta(minutes=30)  # 30-minute time steps
    
    def _update_barge_position(self, barge: Barge):
        """Update the position of a barge in transit"""
        if not barge.current_service:
            return
            
        service = self.services[barge.current_service]
        # Simple simulation: if service duration has passed, move barge to destination
        arrival_time = self.current_time + service.duration
        if arrival_time >= self.current_time:
            barge.current_terminal = service.destination
            barge.status = "unloading"
            barge.current_service = None
    
    def _assign_barge_to_service(self, barge: Barge):
        """Try to assign an idle barge to a service"""
        for service in self.services.values():
            if (service.current_load < service.capacity and 
                barge.current_terminal == service.origin):
                # Check if there are containers waiting at this terminal
                waiting_containers = [
                    c for c in self.containers.values()
                    if c.status == "waiting" and c.origin == service.origin
                ]
                if waiting_containers:
                    barge.status = "loading"
                    barge.current_service = service.id
                    service.current_load += 1
                    break
    
    def _update_container_statuses(self):
        """Update the status of all containers"""
        for container in self.containers.values():
            if container.status == "waiting":
                # Check if container can be loaded onto a barge
                for barge in self.barges.values():
                    if (barge.status == "loading" and 
                        len(barge.containers) < barge.capacity):
                        container.status = "in_transit"
                        barge.containers.append(container.id)
                        break
            elif container.status == "in_transit":
                # Check if container has arrived
                barge_id = next(
                    (b.id for b in self.barges.values() 
                     if container.id in b.containers), None
                )
                if barge_id:
                    barge = self.barges[barge_id]
                    if barge.current_terminal == container.destination:
                        container.status = "delivered"
                        barge.containers.remove(container.id)
    
    def get_performance_metrics(self) -> Dict:
        """Calculate and return performance metrics"""
        total_containers = len(self.containers)
        delivered = len([c for c in self.containers.values() if c.status == "delivered"])
        in_transit = len([c for c in self.containers.values() if c.status == "in_transit"])
        waiting = len([c for c in self.containers.values() if c.status == "waiting"])
        
        active_barges = len([b for b in self.barges.values() if b.status != "idle"])
        terminal_utilization = {
            t.name: (t.current_containers / t.capacity) 
            for t in self.terminals.values()
        }
        
        return {
            "time": self.current_time.strftime("%Y-%m-%d %H:%M"),
            "total_containers": total_containers,
            "delivered": delivered,
            "in_transit": in_transit,
            "waiting": waiting,
            "active_barges": active_barges,
            "terminal_utilization": terminal_utilization
        }
    
    def print_status(self):
        """Print current simulation status"""
        metrics = self.get_performance_metrics()
        print("\n" + "="*50)
        print(f"Simulation Time: {metrics['time']}")
        print("-"*50)
        print(f"Containers Status:")
        print(f"  Total: {metrics['total_containers']}")
        print(f"  Delivered: {metrics['delivered']}")
        print(f"  In Transit: {metrics['in_transit']}")
        print(f"  Waiting: {metrics['waiting']}")
        print(f"\nActive Barges: {metrics['active_barges']}/{len(self.barges)}")
        print("\nTerminal Utilization:")
        for terminal, utilization in metrics['terminal_utilization'].items():
            print(f"  {terminal}: {utilization*100:.1f}%")
        print("="*50)
