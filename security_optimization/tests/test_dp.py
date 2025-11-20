# tests/test_dp.py
import pytest
from models.security_incident import SecurityIncident, IncidentType
from core.dynamic_programming import SecurityResponseOptimizer
from datetime import datetime

class TestDynamicProgramming:
    def test_optimize_response_sequence(self):
        # Cria incidentes de teste
        incidents = [
            SecurityIncident(
                id="1", type=IncidentType.DDOS, severity=0.9, impact=0.8,
                detection_time=datetime.now(), estimated_response_time=30,
                required_resources=[]
            ),
            SecurityIncident(
                id="2", type=IncidentType.SQL_INJECTION, severity=0.7, impact=0.9,
                detection_time=datetime.now(), estimated_response_time=20,
                required_resources=[]
            )
        ]
        
        optimizer = SecurityResponseOptimizer({})
        result = optimizer.optimize_response_sequence(incidents)
        
        assert len(result) <= len(incidents)
        assert all(isinstance(inc, SecurityIncident) for inc in result)