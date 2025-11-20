# models/security_incident.py
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
import uuid
from datetime import datetime

class IncidentType(Enum):
    DDOS = "ddos"
    SQL_INJECTION = "sql_injection"
    MALWARE = "malware"
    DATA_LEAK = "data_leak"
    PHISHING = "phishing"
    RANSOMWARE = "ransomware"

@dataclass
class SecurityIncident:
    id: str
    type: IncidentType
    severity: float  # 0-1 scale
    impact: float    # 0-1 scale
    detection_time: datetime
    estimated_response_time: int  # minutes
    required_resources: List[str]
    priority: float = 0.0
    
    def __post_init__(self):
        if self.priority == 0.0:
            self.calculate_priority()
    
    def calculate_priority(self, w1: float = 0.6, w2: float = 0.4):
        """Calcula prioridade usando fórmula do artigo: Pi = w1·Si + w2·Ii"""
        self.priority = w1 * self.severity + w2 * self.impact
    
    def __lt__(self, other):
        return self.priority > other.priority  # Higher priority first