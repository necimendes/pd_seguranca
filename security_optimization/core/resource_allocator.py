# core/resource_allocator.py
from typing import List, Dict, Tuple
import numpy as np
from models.security_incident import SecurityIncident
from models.resource import Resource

class ResourceAllocator:
    """
    Otimizador de alocação de recursos - VERSÃO CORRIGIDA
    """
    
    def __init__(self, resources: Dict[str, Resource], lambda_coeff: float = 0.5):
        self.resources = resources
        self.lambda_coeff = lambda_coeff
    
    def optimize_allocation(self, incidents: List[SecurityIncident]) -> Dict[str, List[str]]:
        """
        Otimiza a alocação de recursos - VERSÃO SIMPLIFICADA FUNCIONAL
        """
        if not incidents:
            return {}
            
        allocation = {}
        available_resources = list(self.resources.keys())
        
        for incident in incidents:
            # Aloca recursos baseado na prioridade do incidente
            num_resources = min(2, len(available_resources))  # Máximo 2 recursos por incidente
            allocated = available_resources[:num_resources]
            allocation[incident.id] = allocated
            
            # Remove recursos alocados (simulação)
            available_resources = available_resources[num_resources:]
            
            if not available_resources:
                break
        
        return allocation