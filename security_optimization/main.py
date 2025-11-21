# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from models.security_incident import SecurityIncident, IncidentType
from models.resource import Resource, ResourceType
from core.dynamic_programming import SecurityResponseOptimizer
from core.resource_allocator import ResourceAllocator
from core.simulated_annealing import SimulatedAnnealingOptimizer
import uuid

class ComputerSecurityManagementSystem:
    """
    Sistema completo de gestão de segurança otimizada - CORRIGIDO
    """
    
    def __init__(self):
        self.incidents = []
        self.resources = self._initialize_resources()
        self.dp_optimizer = SecurityResponseOptimizer(self.resources)
        self.resource_allocator = ResourceAllocator(self.resources)
        self.sa_optimizer = SimulatedAnnealingOptimizer()
    
    def _initialize_resources(self) -> dict:
        """Inicializa os recursos do sistema"""
        return {
            'computation': Resource(ResourceType.COMPUTATION, capacity=100, cost_per_unit=10),
            'bandwidth': Resource(ResourceType.BANDWIDTH, capacity=50, cost_per_unit=5),
            'storage': Resource(ResourceType.STORAGE, capacity=200, cost_per_unit=2),
            'security_analyst': Resource(ResourceType.ANALYST, capacity=5, cost_per_unit=50)
        }
    
    def add_incident(self, incident_type: IncidentType, severity: float, 
                    impact: float, estimated_response: int, required_resources: list):
        """Adiciona um novo incidente de segurança"""
        incident = SecurityIncident(
            id=str(uuid.uuid4()),
            type=incident_type,
            severity=severity,
            impact=impact,
            detection_time=datetime.now(),
            estimated_response_time=estimated_response,
            required_resources=required_resources
        )
        self.incidents.append(incident)
        print(f"✅ Incidente adicionado: {incident_type.value} (Prioridade: {incident.priority:.2f})")
    
    def optimize_security_management(self):
        """
        Executa a otimização completa do gerenciamento de segurança
        """
        print("=== INICIANDO OTIMIZAÇÃO DE SEGURANÇA ===")
        print(f"Total de incidentes: {len(self.incidents)}")
        
        if not self.incidents:
            print("❌ Nenhum incidente para otimizar!")
            return None
        
        # 1. Otimização da sequência de resposta com PD
        print("\n1. Otimizando sequência de resposta...")
        optimal_sequence = self.dp_optimizer.optimize_response_sequence(self.incidents)
        sequence_types = [inc.type.value for inc in optimal_sequence]
        print(f"📊 Sequência ótima: {sequence_types}")
        print(f"🔢 Incidentes na sequência: {len(optimal_sequence)}/{len(self.incidents)}")
        
        # 2. Otimização de alocação de recursos
        print("\n2. Otimizando alocação de recursos...")
        resource_allocation = self.resource_allocator.optimize_allocation(optimal_sequence)
        print(f"📦 Alocação de recursos: {resource_allocation}")
        
        # 3. Otimização da estratégia com Recozimento Simulado
        print("\n3. Otimizando estratégia de proteção...")
        initial_strategy = {
            'protection_level': 0.7,
            'cost': 1000,
            'resource_allocation': resource_allocation
        }
        optimal_strategy = self.sa_optimizer.optimize_protection_strategy(
            optimal_sequence, initial_strategy
        )
        print(f"🛡️ Estratégia ótima: Nível de proteção {optimal_strategy.get('protection_level', 0)*100:.1f}%")
        
        return {
            'response_sequence': optimal_sequence,
            'resource_allocation': resource_allocation,
            'protection_strategy': optimal_strategy
        }
    
    def generate_performance_report(self, optimization_result: dict):
        """Gera relatório de performance"""
        if not optimization_result:
            return
            
        print("\n" + "="*60)
        print("📈 RELATÓRIO DE PERFORMANCE - SISTEMA DE SEGURANÇA")
        print("="*60)
        
        sequence = optimization_result['response_sequence']
        
        if sequence:
            original_time = sum(inc.estimated_response_time for inc in self.incidents)
            optimized_time = sum(inc.estimated_response_time for inc in sequence)
            
            time_reduction = ((original_time - optimized_time) / original_time) * 100 if original_time > 0 else 0
            resource_utilization = self._calculate_resource_utilization()
            
            print(f"⏱️  Tempo total de resposta: {optimized_time:.1f} min")
            print(f"📉 Redução de tempo: {time_reduction:.1f}%")
            print(f"💾 Utilização média de recursos: {resource_utilization:.1f}%")
            print(f"🔢 Incidentes processados: {len(sequence)}/{len(self.incidents)}")
            print(f"🛡️ Eficiência de proteção: {optimization_result['protection_strategy'].get('protection_level', 0)*100:.1f}%")
            
            # Estatísticas dos incidentes
            high_priority = sum(1 for inc in sequence if inc.priority > 0.7)
            print(f"🎯 Incidentes de alta prioridade tratados: {high_priority}")
        else:
            print("❌ Nenhum incidente foi processado na otimização!")
    
    def _calculate_resource_utilization(self) -> float:
        """Calcula utilização média de recursos"""
        if not self.resources:
            return 0.0
            
        total_utilization = 0
        for resource in self.resources.values():
            utilization = (resource.current_usage / resource.capacity) * 100
            total_utilization += utilization
        
        return total_utilization / len(self.resources)

# Exemplo de uso CORRIGIDO
if __name__ == "__main__":
    # Cria sistema de gestão
    security_system = ComputerSecurityManagementSystem()
    
    print("🚀 INICIALIZANDO SISTEMA DE SEGURANÇA COMPUTACIONAL")
    print("=" * 50)
    
    # Adiciona incidentes de exemplo (conforme artigo)
    security_system.add_incident(
        IncidentType.DDOS, 
        severity=0.9, 
        impact=0.8, 
        estimated_response=30,
        required_resources=['bandwidth', 'computation']
    )
    
    security_system.add_incident(
        IncidentType.SQL_INJECTION,
        severity=0.7,
        impact=0.9,
        estimated_response=20,
        required_resources=['computation', 'security_analyst']
    )
    
    security_system.add_incident(
        IncidentType.MALWARE,
        severity=0.6,
        impact=0.7,
        estimated_response=25,
        required_resources=['storage', 'computation']
    )
    
    security_system.add_incident(
        IncidentType.RANSOMWARE,
        severity=0.95,
        impact=0.9, 
        estimated_response=40,
        required_resources=['computation', 'security_analyst', 'storage']
    )
    
    # Executa otimização completa
    result = security_system.optimize_security_management()
    
    # Gera relatório
    security_system.generate_performance_report(result)
    
    print("\n" + "="*50)
    print("✅ SISTEMA FINALIZADO COM SUCESSO!")
    print("="*50)