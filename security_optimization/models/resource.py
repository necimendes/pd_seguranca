# models/resource.py
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class ResourceType(Enum):
    COMPUTATION = "computation"
    BANDWIDTH = "bandwidth"
    STORAGE = "storage"
    ANALYST = "security_analyst"

@dataclass
class Resource:
    type: ResourceType
    capacity: float
    cost_per_unit: float
    current_usage: float = 0.0
    
    @property
    def available_capacity(self) -> float:
        return self.capacity - self.current_usage
    
    def allocate(self, amount: float) -> bool:
        if amount <= self.available_capacity:
            self.current_usage += amount
            return True
        return False
    
    def release(self, amount: float):
        self.current_usage = max(0, self.current_usage - amount)