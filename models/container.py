from dataclasses import dataclass
from datetime import datetime

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

    def __str__(self):
        return f"Container {self.id[:8]}: {self.status} ({self.type}) - Priority {self.priority}"
