"""
Runbook automatizado para respuesta a incidentes
Basado en los conceptos de gestión de incidentes y recuperación
"""
from typing import Dict, List, Callable, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('incident_response')

class IncidentRunbook:
    """Runbook automatizado para respuesta a incidentes"""
    
    def __init__(self):
        self.incident_types = self._define_incident_types()
        self.escalation_matrix = self._define_escalation()
    
    def _define_incident_types(self) -> Dict:
        """Definir tipos de incidentes y respuestas"""
        return {
            'pipeline_down': {
                'severity': 'CRITICAL',
                'auto_response': True,
                'timeout': timedelta(minutes=15),
                'steps': [
                    'check_airflow_scheduler',
                    'check_database_connectivity', 
                    'restart_failed_services',
                    'verify_pipeline_recovery'
                ]
            },
            'data_quality_degraded': {
                'severity': 'HIGH',
                'auto_response': False,
                'timeout': timedelta(hours=1),
                'steps': [
                    'isolate_affected_data',
                    'check_upstream_sources',
                    'implement_data_filters',
                    'notify_data_consumers'
                ]
            },
            'performance_degraded': {
                'severity': 'MEDIUM',
                'auto_response': True,
                'timeout': timedelta(hours=2),
                'steps': [
                    'check_resource_usage',
                    'scale_resources_if_needed',
                    'optimize_running_queries',
                    'monitor_recovery'
                ]
            }
        }
    
    def _define_escalation(self) -> Dict:
        """Matriz de escalación por tiempo y severidad"""
        return {
            'CRITICAL': {
                '5min': 'alert_lead_engineer',
                '15min': 'alert_engineering_manager',
                '30min': 'alert_vp_engineering'
            },
            'HIGH': {
                '15min': 'alert_lead_engineer',
                '45min': 'alert_engineering_manager'
            },
            'MEDIUM': {
                '30min': 'alert_lead_engineer',
                '2h': 'alert_engineering_manager'
            }
        }
    
    def handle_incident(self, incident_type: str, context: Dict) -> Dict:
        """Manejar incidente según runbook"""
        
        if incident_type not in self.incident_types:
            return {'status': 'unknown_incident_type'}
        
        incident_config = self.incident_types[incident_type]
        start_time = datetime.now()
        
        logger.info(f"Handling {incident_type} incident (severity: {incident_config['severity']})")
        
        results = {
            'incident_type': incident_type,
            'severity': incident_config['severity'],
            'start_time': start_time.isoformat(),
            'steps_executed': [],
            'auto_recovery_attempted': incident_config['auto_response']
        }
        
        # Ejecutar pasos del runbook
        for step in incident_config['steps']:
            step_result = self._execute_step(step, context)
            results['steps_executed'].append(step_result)
            
            if step_result['success']:
                logger.info(f"Step {step} completed successfully")
            else:
                logger.error(f"Step {step} failed: {step_result.get('error')}")
                break
        
        # Verificar resolución
        results['resolved'] = self._verify_resolution(incident_type, context)
        results['end_time'] = datetime.now().isoformat()
        results['duration_seconds'] = (datetime.now() - start_time).total_seconds()
        
        # Escalar si no resuelto
        if not results['resolved']:
            self._escalate_incident(incident_config['severity'], results['duration_seconds'])
        
        return results
    
    def _execute_step(self, step_name: str, context: Dict) -> Dict:
        """Ejecutar paso individual del runbook"""
        
        step_functions = {
            'check_airflow_scheduler': lambda: self._check_service('airflow-scheduler'),
            'check_database_connectivity': lambda: self._check_database_connection(),
            'restart_failed_services': lambda: self._restart_services(['airflow-scheduler', 'airflow-webserver']),
            'verify_pipeline_recovery': lambda: self._verify_pipeline_status(),
            'isolate_affected_data': lambda: self._isolate_bad_data(),
            'check_resource_usage': lambda: self._check_system_resources(),
            'scale_resources_if_needed': lambda: self._scale_resources(),
            'check_upstream_sources': lambda: self._check_upstream_sources(),
            'implement_data_filters': lambda: self._implement_data_filters(),
            'notify_data_consumers': lambda: self._notify_data_consumers(),
            'optimize_running_queries': lambda: self._optimize_running_queries(),
            'monitor_recovery': lambda: self._monitor_recovery()
        }
        
        try:
            step_func = step_functions.get(step_name)
            if step_func:
                result = step_func()
                return {'step': step_name, 'success': True, 'result': result}
            else:
                return {'step': step_name, 'success': False, 'error': 'Step not implemented'}
        except Exception as e:
            return {'step': step_name, 'success': False, 'error': str(e)}
    
    def _escalate_incident(self, severity: str, duration_seconds: float):
        """Escalar incidente según tiempo transcurrido"""
        
        escalation_rules = self.escalation_matrix.get(severity, {})
        
        for time_threshold, action in escalation_rules.items():
            # Convertir tiempo a segundos
            threshold_seconds = self._parse_time_to_seconds(time_threshold)
            
            if duration_seconds >= threshold_seconds:
                logger.warning(f"Escalating {severity} incident: {action}")
                # Aquí iría lógica real de notificación (email, slack, pager, etc.)
    
    # Métodos auxiliares simulados para cada paso del runbook
    
    def _check_service(self, service_name: str) -> Dict:
        """Simular verificación de servicio"""
        return {'status': 'running', 'pid': 12345, 'service': service_name}
    
    def _check_database_connection(self) -> Dict:
        """Simular verificación de conexión a base de datos"""
        return {'connected': True, 'latency_ms': 15, 'database': 'postgresql'}
    
    def _restart_services(self, services: List[str]) -> Dict:
        """Simular reinicio de servicios"""
        return {'restarted': services, 'status': 'success', 'timestamp': datetime.now().isoformat()}
    
    def _verify_pipeline_status(self) -> Dict:
        """Simular verificación de estado de pipelines"""
        return {'pipelines_running': 5, 'pipelines_failed': 0, 'total_pipelines': 5}
    
    def _isolate_bad_data(self) -> Dict:
        """Simular aislamiento de datos corruptos"""
        return {'isolated_records': 150, 'quarantined': True, 'dataset': 'production'}
    
    def _check_system_resources(self) -> Dict:
        """Simular verificación de recursos del sistema"""
        return {'cpu_percent': 45, 'memory_percent': 60, 'disk_percent': 30}
    
    def _scale_resources(self) -> Dict:
        """Simular escalado de recursos"""
        return {'scaled_up': ['airflow-worker'], 'new_instances': 2}
    
    def _check_upstream_sources(self) -> Dict:
        """Simular verificación de fuentes de datos upstream"""
        return {'sources_checked': 3, 'sources_healthy': 3, 'sources_failed': 0}
    
    def _implement_data_filters(self) -> Dict:
        """Simular implementación de filtros de datos"""
        return {'filters_applied': 2, 'records_filtered': 75}
    
    def _notify_data_consumers(self) -> Dict:
        """Simular notificación a consumidores de datos"""
        return {'notified_teams': ['analytics', 'data_science'], 'channels': ['slack', 'email']}
    
    def _optimize_running_queries(self) -> Dict:
        """Simular optimización de consultas en ejecución"""
        return {'queries_optimized': 5, 'performance_improvement': '30%'}
    
    def _monitor_recovery(self) -> Dict:
        """Simular monitoreo de recuperación"""
        return {'monitoring_activated': True, 'metrics_tracked': ['cpu', 'memory', 'latency']}
    
    def _verify_resolution(self, incident_type: str, context: Dict) -> bool:
        """Lógica para verificar si incidente está resuelto"""
        # Simulación: siempre retorna True para demostración
        # En un sistema real, verificaría métricas, logs, etc.
        return True
    
    def _parse_time_to_seconds(self, time_str: str) -> int:
        """Convertir tiempo en formato string a segundos"""
        if 'min' in time_str:
            return int(time_str.replace('min', '')) * 60
        elif 'h' in time_str:
            return int(time_str.replace('h', '')) * 3600
        return 0


# Función para crear template de post-mortem
def create_post_mortem_template(incident_data: Dict) -> str:
    """Crear template de post-mortem basado en incidente"""
    
    # Helper para generar listas
    def generate_list(items, prefix="- "):
        if not items:
            return ""
        return "\n".join(f"{prefix}{item}" for item in items)
    
    def generate_checklist(items, prefix="- [ ] "):
        if not items:
            return ""
        return "\n".join(f"{prefix}{item}" for item in items)
    
    resolution_steps = generate_list(incident_data.get('resolution_steps', []))
    went_well = generate_list(incident_data.get('went_well', []))
    improvements = generate_list(incident_data.get('improvements', []))
    action_items = generate_checklist(incident_data.get('action_items', []))
    prevention = generate_checklist(incident_data.get('prevention', []))
    
    template = f"""
# Post-Mortem: {incident_data.get('title', 'Incidente sin título')}

## Executive Summary
{incident_data.get('summary', 'Descripción del incidente')}

## Timeline
- **Detection**: {incident_data.get('detection_time', 'Desconocido')}
- **Start**: {incident_data.get('start_time', 'Desconocido')}
- **Resolution**: {incident_data.get('end_time', 'Desconocido')}
- **Duration**: {incident_data.get('duration', 'Desconocido')}

## Impact
- **Users Affected**: {incident_data.get('users_affected', 0)}
- **Business Impact**: {incident_data.get('business_impact', 'Desconocido')}
- **Data Loss**: {incident_data.get('data_loss', 'Ninguno')}

## Root Cause Analysis
{incident_data.get('root_cause', 'Por determinar')}

## Resolution Steps
{resolution_steps}

## Lessons Learned
### What went well
{went_well}

### What could be improved
{improvements}

## Action Items
{action_items}

## Prevention Measures
{prevention}

---
*Post-mortem completed on {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    return template
