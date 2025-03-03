from dataclasses import dataclass
from typing import List, Optional

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

    def __str__(self):
        return f"Barge {self.id[:8]}: {self.status} at {self.current_terminal} ({len(self.containers)}/{self.capacity} containers)"
