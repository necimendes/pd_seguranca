# config/settings.py
# Configurações do sistema
OPTIMIZATION_CONFIG = {
    'dp_time_horizon': 10,
    'lambda_coefficient': 0.5,
    'sa_initial_temperature': 1000,
    'sa_cooling_rate': 0.95,
    'max_concurrent_incidents': 5
}

INCIDENT_WEIGHTS = {
    'severity_weight': 0.6,
    'impact_weight': 0.4
}