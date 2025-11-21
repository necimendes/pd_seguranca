# tests/test_dp.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import datetime
from models.security_incident import SecurityIncident, IncidentType
from core.dynamic_programming import SecurityResponseOptimizer

class TestDynamicProgramming:
    def test_optimize_response_sequence_basic(self):
        """Teste básico de otimização de sequência"""
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
        
        assert result is not None
        assert isinstance(result, list)
    
    def test_empty_incidents(self):
        """Teste com lista vazia de incidentes"""
        optimizer = SecurityResponseOptimizer({})
        result = optimizer.optimize_response_sequence([])
        assert result == []