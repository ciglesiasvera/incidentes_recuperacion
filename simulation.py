#!/usr/bin/env python3
"""
Script de simulación para demostrar el manejo de incidentes
Basado en el runbook implementado y conceptos de teoría
"""
import logging
from datetime import datetime
from runbook import IncidentRunbook, create_post_mortem_template

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('simulation')

def simulate_incident_response():
    """Simular respuesta a incidente de pipeline caído"""
    print("=" * 60)
    print("SIMULACIÓN DE RESPUESTA A INCIDENTE")
    print("=" * 60)
    
    # Crear instancia del runbook
    runbook = IncidentRunbook()
    
    # Simular incidente de pipeline caído
    incident_context = {
        'triggered_by': 'alert_pipeline_down',
        'affected_components': ['etl_pipeline', 'data_warehouse'],
        'start_time': datetime.now(),
        'symptoms': ['scheduler_not_responding', 'tasks_queued']
    }
    
    print(f"\n📡 Incidente detectado: 'pipeline_down'")
    print(f"   Desencadenado por: {incident_context['triggered_by']}")
    print(f"   Componentes afectados: {', '.join(incident_context['affected_components'])}")
    print(f"   Síntomas: {', '.join(incident_context['symptoms'])}")
    
    # Ejecutar runbook
    response = runbook.handle_incident('pipeline_down', incident_context)
    
    print("\n📊 RESULTADO DE LA RESPUESTA:")
    print("-" * 40)
    print(f"Tipo: {response['incident_type']}")
    print(f"Severidad: {response['severity']}")
    print(f"Resuelto: {response['resolved']}")
    print(f"Duración: {response['duration_seconds']:.1f}s")
    print(f"Recuperación automática intentada: {response['auto_recovery_attempted']}")
    print(f"Pasos ejecutados: {len(response['steps_executed'])}")
    
    print("\n📝 DETALLE DE PASOS EJECUTADOS:")
    for step in response['steps_executed']:
        status = "✅" if step['success'] else "❌"
        print(f"  {status} {step['step']}")
        if step['success'] and step.get('result'):
            result = step['result']
            if isinstance(result, dict):
                # Mostrar solo algunos detalles importantes
                key = list(result.keys())[0] if result else ''
                print(f"      Resultado: {key} = {result.get(key, 'N/A')}")
    
    return response

def simulate_different_incident_types():
    """Simular diferentes tipos de incidentes"""
    print("\n" + "=" * 60)
    print("SIMULACIÓN DE MÚLTIPLES TIPOS DE INCIDENTES")
    print("=" * 60)
    
    runbook = IncidentRunbook()
    
    incident_types = [
        ('pipeline_down', {
            'triggered_by': 'monitoring_system',
            'affected_components': ['airflow', 'postgresql'],
            'symptoms': ['high_latency', 'timeout_errors']
        }),
        ('data_quality_degraded', {
            'triggered_by': 'data_validation_job',
            'affected_components': ['data_lake', 'analytics_db'],
            'symptoms': ['null_values', 'schema_mismatch']
        }),
        ('performance_degraded', {
            'triggered_by': 'performance_monitor',
            'affected_components': ['compute_cluster', 'cache_layer'],
            'symptoms': ['high_cpu', 'slow_queries']
        })
    ]
    
    for incident_type, context in incident_types:
        print(f"\n🔍 Procesando incidente: {incident_type}")
        response = runbook.handle_incident(incident_type, context)
        
        status = "✅ RESUELTO" if response['resolved'] else "❌ NO RESUELTO"
        print(f"   Estado: {status}")
        print(f"   Pasos ejecutados: {len(response['steps_executed'])}")
        print(f"   Duración: {response['duration_seconds']:.2f}s")

def create_post_mortem_example():
    """Crear ejemplo de post-mortem"""
    print("\n" + "=" * 60)
    print("EJEMPLO DE TEMPLATE POST-MORTEM")
    print("=" * 60)
    
    incident_data = {
        'title': 'Caída del Pipeline ETL - 2024-01-29',
        'summary': 'El pipeline principal de ETL falló debido a un timeout en la conexión a la base de datos upstream, afectando la disponibilidad de datos para reportes críticos.',
        'detection_time': '2024-01-29 14:30 UTC',
        'start_time': '2024-01-29 14:25 UTC',
        'end_time': '2024-01-29 15:45 UTC',
        'duration': '1 hora 20 minutos',
        'users_affected': 150,
        'business_impact': 'Reportes diarios de ventas retrasados, afectando decisiones de inventario',
        'data_loss': '3 horas de datos de transacciones requirieron reprocesamiento',
        'root_cause': 'Timeout de conexión a la base de datos PostgreSQL debido a mantenimiento no comunicado del equipo de infraestructura. La configuración de timeout del pipeline (30s) era insuficiente para el aumento temporal de latencia (45s).',
        'resolution_steps': [
            'Reconexión manual a la base de datos',
            'Reinicio del servicio Airflow Scheduler',
            'Reprocesamiento de datos desde checkpoint',
            'Verificación de integridad de datos'
        ],
        'went_well': [
            'El sistema de alertas detectó el problema en 5 minutos',
            'El equipo de respuesta actuó dentro del SLA',
            'Los datos pudieron recuperarse completamente'
        ],
        'improvements': [
            'Aumentar timeout de conexión a 60s',
            'Implementar retry con backoff exponencial',
            'Mejorar comunicación entre equipos sobre mantenimiento',
            'Crear dashboard de monitoreo de conectividad'
        ],
        'action_items': [
            'Configurar timeout de conexión a 60s',
            'Implementar lógica de retry automático',
            'Crear procedimiento de comunicación de mantenimiento',
            'Desarrollar dashboard de conectividad'
        ],
        'prevention': [
            'Monitoreo proactivo de latencia de conexión',
            'Pruebas de carga regulares',
            'Documentación de procedimientos de failover'
        ]
    }
    
    post_mortem = create_post_mortem_template(incident_data)
    print(post_mortem)
    
    # Guardar ejemplo en archivo
    with open('post_mortem_example.md', 'w') as f:
        f.write(post_mortem)
    print("\n📄 Ejemplo de post-mortem guardado en 'post_mortem_example.md'")
    
    return incident_data

def demonstrate_escalation_logic():
    """Demostrar lógica de escalación"""
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN DE LÓGICA DE ESCALACIÓN")
    print("=" * 60)
    
    runbook = IncidentRunbook()
    
    print("\nMatriz de escalación configurada:")
    for severity, rules in runbook.escalation_matrix.items():
        print(f"\n{severity}:")
        for time_threshold, action in rules.items():
            seconds = runbook._parse_time_to_seconds(time_threshold)
            print(f"  {time_threshold} ({seconds}s) → {action}")
    
    # Simular diferentes duraciones
    print("\nEjemplos de escalación:")
    durations = [
        (60, 'CRITICAL', '1 minuto - dentro del primer umbral'),
        (300, 'CRITICAL', '5 minutos - alerta a lead engineer'),
        (900, 'CRITICAL', '15 minutos - alerta a engineering manager'),
        (1800, 'CRITICAL', '30 minutos - alerta a VP engineering'),
        (120, 'HIGH', '2 minutos - sin escalación'),
        (1200, 'HIGH', '20 minutos - alerta a engineering manager'),
    ]
    
    for duration_seconds, severity, description in durations:
        print(f"\n{description}:")
        print(f"  Duración: {duration_seconds}s")
        print(f"  Severidad: {severity}")
        # Simular llamada a _escalate_incident
        runbook._escalate_incident(severity, duration_seconds)

def main():
    """Función principal de simulación"""
    print("\n🎓 EJERCICIO PRÁCTICO DE GESTIÓN DE INCIDENTES")
    print("📚 Curso Ciencia de Datos Talent Ops")
    
    # Ejecutar simulaciones
    response = simulate_incident_response()
    simulate_different_incident_types()
    create_post_mortem_example()
    demonstrate_escalation_logic()
    
    print("\n" + "=" * 60)
    print("✅ SIMULACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    
    # Resumen final
    print("\n📋 RESUMEN DE LA IMPLEMENTACIÓN:")
    print("• Runbook de incidentes implementado y corregido")
    print("• Lógica de escalación basada en tiempo/severidad")
    print("• Funciones auxiliares simuladas para cada paso")
    print("• Template de post-mortem funcional")
    print("• Demostración completa de todos los conceptos")

if __name__ == "__main__":
    main()