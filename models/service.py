from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class Service:
    id: str
    origin: str  # Terminal ID
    destination: str  # Terminal ID
    capacity: int  # Maximum number of containers
    duration: timedelta
    schedule: List[datetime]  # List of departure times
    current_load: int = 0

    def __str__(self):
        return f"Service {self.origin} -> {self.destination}: {self.current_load}/{self.capacity} containers"
