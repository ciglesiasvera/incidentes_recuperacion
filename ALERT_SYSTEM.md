# Sistema de Alertas y Monitoreo

## 🚨 Arquitectura del Sistema de Alertas

### Componentes Principales

#### 1. **Sistemas de Monitoreo**
- **Datadog:** Métricas, logs, Application Performance Monitoring (APM)
- **CloudWatch:** Métricas de infraestructura AWS
- **Grafana:** Dashboards personalizados para métricas de negocio
- **Prometheus:** Métricas de aplicaciones y servicios

#### 2. **Sistemas de Notificación**
- **PagerDuty:** Gestión principal de alertas y escalación
- **OpsGenie:** Alternativa para equipos específicos
- **Slack:** Comunicación en tiempo real durante incidentes
- **Email:** Notificaciones para incidentes no críticos

#### 3. **Integraciones**
- **Jira:** Creación automática de tickets para incidentes
- **Confluence:** Documentación de incidentes
- **GitHub:** Vinculación con commits y deploys

---

## 🔧 Configuración de Alertas

### Condiciones de Alerta para Pipelines de Datos

```yaml
# Ejemplo de configuración YAML para PagerDuty/Datadog
alert_conditions:
  pipeline_down:
    metric: "airflow.dag_run.duration"
    condition: "avg(last_5m) == 0"
    severity: "CRITICAL"
    notification_channel: "pagerduty_primary"
    
  data_quality_degraded:
    metric: "data.quality.score"
    condition: "avg(last_15m) < 0.95"
    severity: "HIGH"
    notification_channel: "slack_data_team"
    
  performance_degraded:
    metric: "pipeline.execution.time"
    condition: "avg(last_30m) > sla_threshold"
    severity: "MEDIUM"
    notification_channel: "email_engineering"
    
  resource_exhaustion:
    metric: ["cpu.utilization", "memory.utilization", "disk.utilization"]
    condition: "max(last_10m) > 0.85"
    severity: "HIGH"
    notification_channel: "pagerduty_infrastructure"
```

### Configuración de PagerDuty

#### Políticas de Escalación
```json
{
  "escalation_policies": {
    "data_engineering_primary": {
      "levels": [
        {
          "level": 1,
          "delay_in_minutes": 0,
          "targets": [
            {
              "type": "user",
              "id": "lead_engineer_on_call"
            }
          ]
        },
        {
          "level": 2,
          "delay_in_minutes": 15,
          "targets": [
            {
              "type": "user", 
              "id": "engineering_manager"
            }
          ]
        },
        {
          "level": 3,
          "delay_in_minutes": 30,
          "targets": [
            {
              "type": "user",
              "id": "vp_engineering"
            }
          ]
        }
      ]
    }
  }
}
```

#### Reglas de Notificación
- **CRÍTICO:** Llamada telefónica + SMS + Push notification
- **ALTO:** Push notification + Email
- **MEDIO:** Email + Mensaje en Slack
- **BAJO:** Solo email (horario laboral)

---

## 🔌 Integración con el Runbook

### Flujo de Alerta → Runbook Automatizado

```
[Monitor] → [Detección] → [PagerDuty] → [Runbook] → [Resolución]
     ↓           ↓           ↓             ↓           ↓
  Métricas    Condición   Notificación  Ejecución   Verificación
```

### Implementación en Código

```python
class AlertSystem:
    """Integración con sistemas de alertas externos"""
    
    def __init__(self):
        # Configuración de clientes para sistemas de alertas
        self.pagerduty_client = PagerDutyClient(api_key=os.getenv('PAGERDUTY_API_KEY'))
        self.slack_client = SlackClient(token=os.getenv('SLACK_TOKEN'))
        
    def trigger_incident(self, incident_type: str, severity: str, context: Dict) -> str:
        """Disparar incidente en sistema de alertas"""
        
        # Mapear severidad a niveles de PagerDuty
        severity_mapping = {
            'CRITICAL': 'critical',
            'HIGH': 'error', 
            'MEDIUM': 'warning',
            'LOW': 'info'
        }
        
        # Crear incidente en PagerDuty
        incident_data = {
            'type': 'incident',
            'title': f'Incidente {incident_type} - {severity}',
            'service': {'id': 'data_pipeline_service'},
            'priority': {'id': self._get_priority_id(severity)},
            'body': {
                'type': 'incident_body',
                'details': json.dumps(context)
            }
        }
        
        response = self.pagerduty_client.create_incident(incident_data)
        
        # Notificar en Slack
        self._notify_slack(incident_type, severity, context, response['incident_number'])
        
        return response['incident_number']
    
    def escalate_incident(self, incident_id: str, escalation_level: str):
        """Escalar incidente según matriz definida"""
        
        escalation_actions = {
            'alert_lead_engineer': {
                'action': 'add_responder',
                'user_id': 'lead_engineer_id'
            },
            'alert_engineering_manager': {
                'action': 'escalate',
                'policy_id': 'engineering_manager_policy'
            },
            'alert_vp_engineering': {
                'action': 'escalate',
                'policy_id': 'vp_engineering_policy'
            }
        }
        
        if escalation_level in escalation_actions:
            action = escalation_actions[escalation_level]
            self.pagerduty_client.update_incident(incident_id, action)
```

---

## 📊 Dashboard de Monitoreo

### Métricas Esenciales para Pipelines

#### 1. **Disponibilidad del Pipeline**
```python
metrics = {
    'pipeline_uptime': '100 * (successful_runs / total_runs)',
    'sla_compliance': '100 * (on_time_completions / total_runs)',
    'failure_rate': '100 * (failed_runs / total_runs)'
}
```

#### 2. **Calidad de Datos**
```python
quality_metrics = {
    'completeness': '100 * (non_null_records / total_records)',
    'accuracy': '100 * (valid_records / total_records)',
    'timeliness': 'seconds_between(expected_time, actual_time)'
}
```

#### 3. **Performance**
```python
performance_metrics = {
    'execution_time': 'end_time - start_time',
    'throughput': 'records_processed / execution_time',
    'resource_utilization': 'max(cpu, memory, disk, network)'
}
```

### Dashboard en Grafana

**URL:** `https://grafana.company.com/dashboards/data-pipelines`

**Paneles principales:**
1. **Resumen de Salud:** Estado global de todos los pipelines
2. **Tiempos de Ejecución:** Gráficos de tendencia por pipeline
3. **Tasas de Error:** Alertas por tipo de error
4. **Utilización de Recursos:** CPU, memoria, disco, red
5. **SLA Compliance:** Cumplimiento de acuerdos de nivel de servicio

---

## 🛠️ Implementación Práctica

### Configuración de Alertas en Código

```python
# alert_config.py
ALERT_CONFIG = {
    'pipeline_down': {
        'monitoring_tool': 'datadog',
        'query': 'avg:airflow.dag_run.duration{env:production} by {dag_id}.fill(zero) < 1',
        'threshold': 300,  # 5 minutos en segundos
        'notification': {
            'pagerduty': {
                'service_key': 'data-pipeline-service',
                'escalation_policy': 'data-engineering-primary'
            },
            'slack': {
                'channel': '#data-alerts',
                'severity': 'critical'
            }
        }
    },
    'data_quality': {
        'monitoring_tool': 'custom',
        'query': 'SELECT * FROM data_quality_metrics WHERE score < 0.95',
        'threshold': 0.95,
        'notification': {
            'pagerduty': {
                'service_key': 'data-quality-service',
                'escalation_policy': 'data-engineering-secondary'
            }
        }
    }
}
```

### Automatización de Respuesta

```python
# automated_response.py
def automated_incident_response(alert_data):
    """Respuesta automatizada a alertas"""
    
    # Parsear alerta
    incident_type = alert_data.get('incident_type')
    severity = alert_data.get('severity')
    
    # Inicializar runbook
    runbook = IncidentRunbook()
    
    # Contexto para el runbook
    context = {
        'alert_id': alert_data['id'],
        'triggered_by': alert_data['source'],
        'detection_time': alert_data['timestamp'],
        'metric_values': alert_data.get('metrics', {})
    }
    
    # Ejecutar runbook
    result = runbook.handle_incident(incident_type, context)
    
    # Actualizar estado en PagerDuty
    update_incident_status(
        alert_data['pagerduty_incident_id'],
        'investigating' if not result['resolved'] else 'resolved',
        result
    )
    
    return result
```

---

## 📈 Métricas del Sistema de Alertas

### KPIs de Efectividad
1. **Tiempo Medio de Detección (MTTD):** < 5 minutos
2. **Tiempo Medio de Acknowledge (MTTA):** < 10 minutos
3. **Tasa de Falsos Positivos:** < 5%
4. **Cobertura de Monitoreo:** > 95% de componentes críticos
5. **Automatización de Respuesta:** > 70% de incidentes

### Reportes Regulares
- **Diario:** Resumen de alertas del día anterior
- **Semanal:** Análisis de tendencias y falsos positivos
- **Mensual:** Revisión de políticas y ajuste de thresholds

---

## 🔒 Seguridad y Compliance

### Control de Accesos
- **Principio de Mínimo Privilegio:** Solo equipo autorizado puede modificar alertas
- **Auditoría:** Log de todos los cambios en configuración de alertas
- **Rotación de Credenciales:** API keys rotadas cada 90 días

### Cumplimiento Normativo
- **SOX:** Alertas para transacciones financieras
- **GDPR:** Monitoreo de acceso a datos personales
- **HIPAA:** Alertas para acceso a datos de salud

---

## 🚨 Procedimientos de Emergencia

### Fallo del Sistema de Alertas
1. **Backup de Notificaciones:** Sistema secundario (OpsGenie)
2. **Procedimiento Manual:** Activación vía teléfono/WhatsApp
3. **Monitoreo del Monitoreo:** Alertas para sistema de alertas caído

### Mantenimiento Programado
1. **Ventana de Mantenimiento:** Domingos 2:00-4:00 AM
2. **Notificación Previa:** 72 horas antes vía email
3. **Procedimiento de Handoff:** Transferencia a equipo secundario

---

*Documento actualizado: Enero 2026*  
*Propietario: Site Reliability Engineering (SRE)*  
*Revisión próxima: Cada 6 meses*