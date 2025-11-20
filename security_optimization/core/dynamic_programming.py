# core/dynamic_programming.py
from typing import List, Dict, Tuple
import numpy as np
from models.security_incident import SecurityIncident
from models.resource import Resource

class SecurityResponseOptimizer:
    """
    Otimizador de resposta a incidentes usando Programação Dinâmica
    Implementa o modelo descrito no artigo
    """
    
    def __init__(self, resources: Dict[str, Resource], time_horizon: int = 10):
        self.resources = resources
        self.time_horizon = time_horizon
        
    def optimize_response_sequence(self, incidents: List[SecurityIncident]) -> List[SecurityIncident]:
        """
        Otimiza a sequência de resposta usando PD
        Retorna a ordem ótima de resposta
        """
        if not incidents:
            return []
            
        # Ordena incidentes por prioridade inicial
        sorted_incidents = sorted(incidents, reverse=True)
        
        # Matriz de programação dinâmica
        n = len(sorted_incidents)
        dp = np.zeros((n + 1, self.time_horizon + 1))
        decisions = np.zeros((n + 1, self.time_horizon + 1), dtype=int)
        
        # Preenche a tabela DP
        for i in range(1, n + 1):
            incident = sorted_incidents[i - 1]
            for t in range(1, self.time_horizon + 1):
                # Opção 1: Não responder ao incidente i no tempo t
                option1 = dp[i - 1][t]
                
                # Opção 2: Responder ao incidente i no tempo t
                resource_available = self._check_resources_availability(incident)
                if resource_available and t >= incident.estimated_response_time:
                    protection_effect = incident.priority * incident.severity
                    cost = self._calculate_response_cost(incident)
                    option2 = dp[i - 1][t - incident.estimated_response_time] + protection_effect - cost
                else:
                    option2 = -float('inf')
                
                # Escolhe a melhor opção
                if option1 >= option2:
                    dp[i][t] = option1
                    decisions[i][t] = 0
                else:
                    dp[i][t] = option2
                    decisions[i][t] = 1
        
        # Reconstrói a sequência ótima
        optimal_sequence = self._reconstruct_sequence(decisions, sorted_incidents)
        return optimal_sequence
    
    def _check_resources_availability(self, incident: SecurityIncident) -> bool:
        """Verifica se há recursos disponíveis para responder ao incidente"""
        # Simulação simplificada - implementação real verificaria cada recurso
        total_required = incident.severity * incident.impact
        available = sum(res.available_capacity for res in self.resources.values())
        return available >= total_required
    
    def _calculate_response_cost(self, incident: SecurityIncident) -> float:
        """Calcula o custo de resposta ao incidente"""
        base_cost = incident.severity * 100  # Custo base por severidade
        resource_cost = len(incident.required_resources) * 50
        return base_cost + resource_cost
    
    def _reconstruct_sequence(self, decisions: np.ndarray, incidents: List[SecurityIncident]) -> List[SecurityIncident]:
        """Reconstrói a sequência ótima a partir da matriz de decisões"""
        sequence = []
        i, t = len(incidents), self.time_horizon
        
        while i > 0 and t > 0:
            if decisions[i][t] == 1:
                sequence.append(incidents[i - 1])
                t -= incidents[i - 1].estimated_response_time
            i -= 1
        
        return list(reversed(sequence))