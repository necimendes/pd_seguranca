# core/incident_prioritization.py
from typing import List
from models.security_incident import SecurityIncident

class IncidentPrioritizer:
    """
    Classe para priorização de incidentes de segurança
    Implementa a fórmula de prioridade do artigo: Pi = w1·Si + w2·Ii
    """
    
    def __init__(self, severity_weight: float = 0.6, impact_weight: float = 0.4):
        self.severity_weight = severity_weight
        self.impact_weight = impact_weight
    
    def calculate_priorities(self, incidents: List[SecurityIncident]) -> List[SecurityIncident]:
        """
        Calcula e atualiza as prioridades de todos os incidentes
        """
        for incident in incidents:
            incident.calculate_priority(self.severity_weight, self.impact_weight)
        
        return sorted(incidents, reverse=True)  # Ordena por prioridade (maior primeiro)
    
    def get_high_priority_incidents(self, incidents: List[SecurityIncident], 
                                  threshold: float = 0.7) -> List[SecurityIncident]:
        """
        Retorna incidentes com prioridade acima do threshold
        """
        return [inc for inc in incidents if inc.priority >= threshold]