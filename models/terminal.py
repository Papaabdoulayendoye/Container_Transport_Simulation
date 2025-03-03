from dataclasses import dataclass

@dataclass
class Terminal:
    id: str
    name: str
    capacity: int  # Maximum number of containers that can be stored
    current_containers: int = 0

    def __str__(self):
        return f"Terminal {self.name}: {self.current_containers}/{self.capacity} containers"
