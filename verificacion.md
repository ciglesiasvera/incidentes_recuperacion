Gestión de Incidentes y Recuperación
Ejercicio: Crear plan de respuesta a incidentes

============================================================
RESPUESTAS A PREGUNTAS DE VERIFICACIÓN
============================================================

1. ¿Cuál es la diferencia entre un incidente que requiere respuesta inmediata vs uno que puede esperar?

RESPUESTA:

    La diferencia clave radica en el IMPACTO y la URGENCIA:

    Incidente que requiere respuesta inmediata (CRÍTICO/ALTO):
    • Impacto directo en usuarios, clientes o ingresos
    • Violación de SLA/SLO críticos
    • Degradación significativa del servicio
    • Pérdida o corrupción de datos
    • Tiempo de resolución medido en minutos
    • Ejemplos: Caída de pipeline de producción, datos corruptos afectando reportes financieros
    
    Incidente que puede esperar (MEDIO/BAJO):
    • Impacto limitado o no crítico
    • Degradación menor del servicio
    • No afecta funcionalidad core del negocio
    • Puede manejarse en horario laboral normal
    • Tiempo de resolución medido en horas/días
    • Ejemplos: Degradación de performance no crítica, problemas de datos históricos
    
    Factores de decisión según la teoría:
    • Severidad del impacto en usuarios/negocio
    • Tiempo estimado de resolución
    • Disponibilidad de workarounds
    • Hora del día/día de la semana
    • Recursos disponibles para respuesta
    

2. ¿Cómo decidir cuándo escalar un incidente a niveles superiores?

RESPUESTA:

    La decisión de escalar se basa en una combinación de FACTORES DE TIEMPO y SEVERIDAD:

    Criterios basados en tiempo (matriz de escalación):
    • Límites de tiempo predefinidos por severidad (5min/15min/30min)
    • Tiempo transcurrido sin progreso en resolución
    • Tiempo estimado para resolución excede umbrales
    
    Criterios basados en severidad/impacto:
    • Incidente CRÍTICO que afecta múltiples sistemas
    • Impacto financiero significativo
    • Exposición de datos sensibles o seguridad comprometida
    • Falta de expertise o autoridad en equipo actual
    
    Criterios basados en recursos:
    • Equipo inicial no tiene habilidades necesarias
    • Requiere aprobaciones de gasto o cambios
    • Necesita coordinación con equipos externos
    • Requiere decisiones estratégicas de negocio
    
    Proceso de decisión:
    1. Monitorear tiempo transcurrido vs. umbrales de escalación
    2. Evaluar progreso real en resolución
    3. Considerar impacto creciente en usuarios/negocio
    4. Verificar disponibilidad de recursos y expertise
    5. Seguir runbook documentado de escalación
    
    La teoría enfatiza:
    • Establecer umbrales CLAROS y DOCUMENTADOS
    • Evitar escalación prematura (ruido innecesario)
    • Evitar escalación tardía (impacto innecesario)
    • Comunicación proactiva durante la escalación
    
