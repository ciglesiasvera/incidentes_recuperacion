# Documentación de Runbooks de Incidentes

## 📋 Descripción General

Los runbooks implementados en este proyecto automatizan la respuesta a incidentes comunes en pipelines de datos. Cada runbook sigue un enfoque estructurado de detección, diagnóstico, recuperación y verificación.

---

## 🚨 Tipos de Incidentes Soportados

### 1. **Pipeline Down (CRÍTICO)**
**Descripción:** Caída completa o parcial de pipelines de datos en producción
**Umbral de detección:** Pipeline inactivo por más de 5 minutos
**SLAs:** Resolución en menos de 30 minutos

#### Pasos del Runbook:
1. **check_airflow_scheduler:** Verificar estado del scheduler de Airflow
2. **check_database_connectivity:** Validar conectividad con bases de datos
3. **restart_failed_services:** Reiniciar servicios fallidos
4. **verify_pipeline_recovery:** Verificar recuperación del pipeline

#### Matriz de Escalación:
- **5 minutos:** Alertar a Lead Engineer
- **15 minutos:** Alertar a Engineering Manager  
- **30 minutos:** Alertar a VP Engineering

---

### 2. **Data Quality Degraded (ALTO)**
**Descripción:** Degradación significativa en la calidad de datos
**Umbral de detección:** Score de calidad < 95%
**SLAs:** Diagnóstico en menos de 1 hora

#### Pasos del Runbook:
1. **isolate_affected_data:** Aislar datos afectados/corruptos
2. **check_upstream_sources:** Verificar fuentes de datos upstream
3. **implement_data_filters:** Implementar filtros de datos
4. **notify_data_consumers:** Notificar a consumidores de datos

#### Matriz de Escalación:
- **15 minutos:** Alertar a Lead Engineer
- **45 minutos:** Alertar a Engineering Manager

---

### 3. **Performance Degraded (MEDIO)**
**Descripción:** Degradación de performance que afecta SLAs
**Umbral de detección:** Tiempo de ejecución > 120% del baseline
**SLAs:** Mejora en menos de 2 horas

#### Pasos del Runbook:
1. **check_resource_usage:** Verificar uso de recursos del sistema
2. **scale_resources_if_needed:** Escalar recursos si es necesario
3. **optimize_running_queries:** Optimizar consultas en ejecución
4. **monitor_recovery:** Monitorear recuperación

#### Matriz de Escalación:
- **30 minutos:** Alertar a Lead Engineer
- **2 horas:** Alertar a Engineering Manager

---

## 🔧 Acceso a los Runbooks

### Método 1: Uso Directo del Código
```python
from runbook import IncidentRunbook

# Inicializar runbook
runbook = IncidentRunbook()

# Manejar incidente
context = {
    'triggered_by': 'monitoring_system',
    'affected_components': ['etl_pipeline'],
    'symptoms': ['high_latency', 'timeout_errors']
}

response = runbook.handle_incident('pipeline_down', context)
print(f"Incidente resuelto: {response['resolved']}")
```

### Método 2: CLI Integrado
```bash
# Ejecutar runbook desde línea de comandos
python -m runbook_cli --incident-type pipeline_down --context '{"triggered_by": "alert"}'
```

### Método 3: API REST (Simulada)
```python
# Ejemplo de endpoint REST
@app.route('/api/v1/incidents', methods=['POST'])
def handle_incident():
    data = request.json
    runbook = IncidentRunbook()
    result = runbook.handle_incident(data['type'], data['context'])
    return jsonify(result)
```

---

## 🛠️ Configuración y Personalización

### Modificar Tipos de Incidentes
```python
# Extender la clase para agregar nuevos tipos de incidentes
class CustomIncidentRunbook(IncidentRunbook):
    def _define_incident_types(self):
        types = super()._define_incident_types()
        types['security_breach'] = {
            'severity': 'CRITICAL',
            'auto_response': False,
            'timeout': timedelta(minutes=10),
            'steps': [
                'isolate_system',
                'collect_forensic_data',
                'notify_security_team',
                'implement_containment'
            ]
        }
        return types
```

### Configurar Matriz de Escalación
```python
# Personalizar matriz de escalación
class CustomEscalationRunbook(IncidentRunbook):
    def _define_escalation(self):
        return {
            'CRITICAL': {
                '3min': 'alert_sre_primary',
                '10min': 'alert_sre_secondary',
                '20min': 'alert_cto'
            },
            # ... otras personalizaciones
        }
```

---

## 📊 Métricas y Monitoreo de Runbooks

### Métricas Recopiladas
Cada ejecución de runbook genera métricas que pueden ser consumidas por sistemas de monitoreo:

```python
# Ejemplo de métricas generadas
runbook_metrics = {
    'incident_type': 'pipeline_down',
    'severity': 'CRITICAL',
    'start_time': '2024-01-29T14:30:00Z',
    'end_time': '2024-01-29T14:45:00Z',
    'duration_seconds': 900,
    'steps_executed': 4,
    'steps_successful': 4,
    'steps_failed': 0,
    'auto_recovery_attempted': True,
    'resolved': True,
    'escalation_required': False
}
```

### Integración con Sistemas de Monitoreo
```python
# Enviar métricas a Datadog
def send_metrics_to_datadog(metrics):
    datadog_client.gauge('runbook.duration', metrics['duration_seconds'])
    datadog_client.gauge('runbook.steps.total', metrics['steps_executed'])
    datadog_client.gauge('runbook.steps.successful', metrics['steps_successful'])
    datadog_client.event(
        title=f"Runbook {metrics['incident_type']} completed",
        text=f"Resolved: {metrics['resolved']} in {metrics['duration_seconds']}s",
        alert_type='success' if metrics['resolved'] else 'error'
    )
```

---

## 🔄 Flujos de Trabajo

### Flujo Normal de Ejecución
```
[Detectar Incidente] → [Clasificar Severidad] → [Ejecutar Runbook] → [Verificar Resolución] → [Documentar Post-Mortem]
```

### Flujo con Escalación
```
[Ejecutar Runbook] → [Monitorear Progreso] → [¿Resuelto en Tiempo?] → [NO] → [Escalar según Matriz] → [Re-ejecutar Pasos]
```

---

## 🧪 Pruebas y Validación

### Pruebas Unitarias
```python
def test_pipeline_down_runbook():
    """Probar runbook de pipeline caído"""
    runbook = IncidentRunbook()
    context = {'triggered_by': 'test', 'affected_components': ['test_pipeline']}
    
    response = runbook.handle_incident('pipeline_down', context)
    
    assert response['incident_type'] == 'pipeline_down'
    assert response['severity'] == 'CRITICAL'
    assert len(response['steps_executed']) == 4
    assert all(step['success'] for step in response['steps_executed'])
```

### Simulaciones Periódicas
```bash
# Ejecutar simulación mensual
python simulation.py --test-mode --incident-type pipeline_down

# Ejecutar simulación de todos los tipos
python simulation.py --comprehensive-test
```

---

## 📈 Mejora Continua

### Revisión de Runbooks
- **Mensual:** Revisar efectividad de pasos actuales
- **Trimestral:** Analizar métricas de éxito/failure
- **Anual:** Rediseñar runbooks basado en lecciones aprendidas

### Proceso de Actualización
1. **Propuesta de Cambio:** Documentar en PR de GitHub
2. **Revisión por Pares:** Equipo de SRE + Engineering Manager
3. **Pruebas:** Simulación completa antes de implementación
4. **Implementación:** Merge a branch principal
5. **Comunicación:** Notificar a todos los equipos afectados

---

## 🔗 Integraciones

### Con Sistemas de Alertas
```python
# Integración con PagerDuty
def pagerduty_to_runbook(pagerduty_alert):
    """Convertir alerta de PagerDuty a contexto de runbook"""
    return {
        'incident_type': map_alert_to_incident_type(pagerduty_alert),
        'severity': pagerduty_alert['severity'],
        'context': {
            'pagerduty_incident_id': pagerduty_alert['id'],
            'triggered_by': 'pagerduty',
            'description': pagerduty_alert['description']
        }
    }
```

### Con Sistemas de Ticketing
```python
# Crear ticket en Jira automáticamente
def create_jira_ticket_from_runbook(runbook_result):
    """Crear ticket de seguimiento en Jira"""
    jira_client.create_issue(
        project='INCIDENT',
        summary=f"Incidente {runbook_result['incident_type']}",
        description=generate_post_mortem_summary(runbook_result),
        issuetype={'name': 'Incident'}
    )
```

---

## 🚨 Procedimientos de Emergencia

### Runbook No Disponible
1. **Procedimiento Manual:** Siguientes pasos documentados en wiki interna
2. **Contactos de Emergencia:** Lista telefónica actualizada
3. **Documentación de Backup:** Copias impresas en ubicación segura

### Sistema de Runbooks Caído
1. **Failover Automático:** Sistema secundario en región diferente
2. **Modo Degradado:** Funcionalidad básica via CLI
3. **Procedimiento de Recuperación:** Restaurar desde backups automáticos

---

## 📚 Recursos Adicionales

### Documentación Relacionada
- [ALERT_SYSTEM.md](./ALERT_SYSTEM.md): Sistema de alertas configurado
- [RESPONSE_TEAM.md](./RESPONSE_TEAM.md): Equipo de respuesta definido
- [post_mortem_example.md](./post_mortem_example.md): Ejemplo de post-mortem

### Enlaces Externos
- **Wiki Interna:** https://wiki.company.com/runbooks
- **Dashboard de Métricas:** https://grafana.company.com/dashboards/runbooks
- **Repositorio de Runbooks:** https://github.com/company/runbooks

---

## 📞 Soporte y Contacto

### Canal de Soporte
- **Slack:** `#runbook-support`
- **Email:** `runbooks@company.com`
- **Horario:** 24/7 para incidentes CRÍTICOS

### Propietario del Runbook
- **Rol:** Site Reliability Engineering (SRE)
- **Responsable:** Engineering Manager
- **Revisión:** Cada 3 meses

---

*Documento actualizado: Enero 2026*  
*Versión: 2.1.0*  
*Próxima revisión: Abril 2026*