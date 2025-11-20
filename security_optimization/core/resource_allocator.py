# core/resource_allocator.py
from typing import List, Dict, Tuple
import numpy as np
from models.security_incident import SecurityIncident
from models.resource import Resource

class ResourceAllocator:
    """
    Otimizador de alocação de recursos usando Programação Dinâmica
    Implementa a fórmula (2) do artigo: Minimize custo, maximize proteção
    """
    
    def __init__(self, resources: Dict[str, Resource], lambda_coeff: float = 0.5):
        self.resources = resources
        self.lambda_coeff = lambda_coeff  # Coeficiente de compensação
    
    def optimize_allocation(self, incidents: List[SecurityIncident]) -> Dict[str, List[str]]:
        """
        Otimiza a alocação de recursos para múltiplos incidentes
        Retorna dicionário com alocação por incidente
        """
        n = len(incidents)
        m = len(self.resources)
        
        # Matriz DP: dp[i][j] = melhor valor para i incidentes com j recursos
        dp = np.zeros((n + 1, m + 1))
        allocation = np.zeros((n + 1, m + 1), dtype=object)
        
        resource_list = list(self.resources.keys())
        
        for i in range(1, n + 1):
            incident = incidents[i - 1]
            for j in range(1, m + 1):
                # Para cada combinação de incidente e recurso
                for k in range(j + 1):
                    current_resource = resource_list[k - 1] if k > 0 else None
                    
                    if current_resource:
                        cost = self.resources[current_resource].cost_per_unit
                        protection_effect = self._calculate_protection_effect(incident, current_resource)
                        
                        # Função objetivo do artigo
                        value = protection_effect - self.lambda_coeff * cost
                    else:
                        value = 0
                    
                    # Atualiza DP
                    if value + dp[i - 1][j - k] > dp[i][j]:
                        dp[i][j] = value + dp[i - 1][j - k]
                        allocation[i][j] = (i - 1, k)
        
        # Reconstrói alocação ótima
        optimal_allocation = self._reconstruct_allocation(allocation, incidents, resource_list)
        return optimal_allocation
    
    def _calculate_protection_effect(self, incident: SecurityIncident, resource: str) -> float:
        """Calcula o efeito de proteção do recurso no incidente"""
        base_effect = incident.priority * 10
        resource_multiplier = {
            'computation': 1.2,
            'bandwidth': 1.5 if incident.type.value == 'ddos' else 1.0,
            'storage': 1.1,
            'security_analyst': 2.0
        }
        return base_effect * resource_multiplier.get(resource, 1.0)
    
    def _reconstruct_allocation(self, allocation: np.ndarray, incidents: List[SecurityIncident], 
                              resources: List[str]) -> Dict[str, List[str]]:
        """Reconstrói a alocação ótima de recursos"""
        result = {}
        i, j = len(incidents), len(resources)
        
        while i > 0 and j > 0:
            incident_idx, resource_count = allocation[i][j]
            incident = incidents[incident_idx]
            
            if incident.id not in result:
                result[incident.id] = []
            
            # Adiciona recursos alocados
            for k in range(resource_count):
                if k < len(resources):
                    result[incident.id].append(resources[k])
            
            j -= resource_count
            i -= 1
        
        return result