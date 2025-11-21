# security_optimization/models/__init__.py
from .security_incident import SecurityIncident, IncidentType
from .resource import Resource, ResourceType

__all__ = [
    'SecurityIncident',
    'IncidentType',
    'Resource', 
    'ResourceType'
]