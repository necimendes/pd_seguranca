# core/simulated_annealing.py
import math
import random
from typing import List, Dict, Tuple, Any
import numpy as np
from models.security_incident import SecurityIncident

class SimulatedAnnealingOptimizer:
    """
    Implementação do algoritmo de Recozimento Simulado para otimização global
    da estratégia de proteção (conforme descrito no artigo)
    """
    
    def __init__(self, initial_temperature: float = 1000, cooling_rate: float = 0.95,
                 min_temperature: float = 1e-3, max_iterations: int = 1000):
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.max_iterations = max_iterations
    
    def optimize_protection_strategy(self, incidents: List[SecurityIncident], 
                                   current_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Otimiza a estratégia de proteção usando recozimento simulado
        """
        current_solution = current_strategy.copy()
        current_energy = self._evaluate_solution(current_solution, incidents)
        
        best_solution = current_solution.copy()
        best_energy = current_energy
        
        temperature = self.initial_temperature
        iteration = 0
        
        while temperature > self.min_temperature and iteration < self.max_iterations:
            # Gera solução vizinha
            neighbor_solution = self._get_neighbor_solution(current_solution)
            neighbor_energy = self._evaluate_solution(neighbor_solution, incidents)
            
            # Decide se aceita a nova solução
            energy_difference = neighbor_energy - current_energy
            if energy_difference > 0 or random.random() < math.exp(energy_difference / temperature):
                current_solution = neighbor_solution
                current_energy = neighbor_energy
                
                if current_energy > best_energy:
                    best_solution = current_solution.copy()
                    best_energy = current_energy
            
            # Resfria o sistema
            temperature *= self.cooling_rate
            iteration += 1
        
        return best_solution
    
    def _evaluate_solution(self, solution: Dict[str, Any], incidents: List[SecurityIncident]) -> float:
        """
        Avalia a qualidade da solução (função objetivo)
        Implementa a fórmula (3) do artigo: Vt(s) = max[R(s,d) + γ·Vt+1(s+1)]
        """
        total_value = 0.0
        gamma = 0.9  # Fator de desconto
        
        for incident in incidents:
            immediate_reward = self._calculate_immediate_reward(solution, incident)
            future_value = self._estimate_future_value(solution, incident)
            total_value += immediate_reward + gamma * future_value
        
        return total_value
    
    def _calculate_immediate_reward(self, solution: Dict[str, Any], incident: SecurityIncident) -> float:
        """Calcula a recompensa imediata R(s,d)"""
        protection_score = solution.get('protection_level', 0.5) * incident.priority
        cost_penalty = solution.get('cost', 0) * 0.1
        return protection_score - cost_penalty
    
    def _estimate_future_value(self, solution: Dict[str, Any], incident: SecurityIncident) -> float:
        """Estima o valor futuro Vt+1(s+1)"""
        # Simulação simplificada - implementação real seria mais complexa
        return incident.severity * 0.8
    
    def _get_neighbor_solution(self, current_solution: Dict[str, Any]) -> Dict[str, Any]:
        """Gera uma solução vizinha perturbando a solução atual"""
        neighbor = current_solution.copy()
        
        # Perturba parâmetros aleatórios
        if 'protection_level' in neighbor:
            neighbor['protection_level'] = max(0.1, min(1.0, 
                neighbor['protection_level'] + random.uniform(-0.1, 0.1)))
        
        if 'resource_allocation' in neighbor:
            # Perturba alocação de recursos
            pass
        
        return neighbor