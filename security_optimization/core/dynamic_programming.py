# core/dynamic_programming.py
from typing import List, Dict, Tuple
import numpy as np
from models.security_incident import SecurityIncident
from models.resource import Resource

class SecurityResponseOptimizer:
    """
    Otimizador de resposta a incidentes usando Programação Dinâmica - CORRIGIDO
    """
    
    def __init__(self, resources: Dict[str, Resource], time_horizon: int = 100):
        self.resources = resources
        self.time_horizon = time_horizon
        
    def optimize_response_sequence(self, incidents: List[SecurityIncident]) -> List[SecurityIncident]:
        """
        Otimiza a sequência de resposta usando PD - VERSÃO CORRIGIDA
        """
        if not incidents:
            return []
            
        n = len(incidents)
        
        # Pré-calcula valores para cada incidente
        incident_values = []
        for incident in incidents:
            value = incident.priority * 100  # Valor baseado na prioridade
            time_required = incident.estimated_response_time
            incident_values.append((value, time_required, incident))
        
        # Matriz DP: dp[t] = máximo valor alcançável no tempo t
        dp = [0] * (self.time_horizon + 1)
        decisions = [[] for _ in range(self.time_horizon + 1)]
        
        # Algoritmo da mochila adaptado para sequenciamento
        for i in range(n):
            value, time_req, incident = incident_values[i]
            for t in range(self.time_horizon, time_req - 1, -1):
                if dp[t] < dp[t - time_req] + value:
                    dp[t] = dp[t - time_req] + value
                    decisions[t] = decisions[t - time_req] + [incident]
        
        # Encontra a melhor solução
        best_time = np.argmax(dp)
        optimal_sequence = decisions[best_time]
        
        return optimal_sequence
    
    def _check_resources_availability(self, incident: SecurityIncident) -> bool:
        """Verifica se há recursos disponíveis"""
        # Simulação - sempre retorna True para teste
        return True