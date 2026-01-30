# Sistema de Gestión de Incidentes y Recuperación

## 📋 Información del Proyecto

**Proyecto:** `incidentes_recuperacion`  
**Autor:** Cristian Iglesias  
**Rol:** Técnico de Nivel Superior en Producción de Software | Desarrollador Full Stack Python | Docente de Informática en la Universidad Católica de Temuco | Relator de Bootcamp Full Stack Python

**Curso:** Ciencia de Datos - Talent Ops  
**Módulo:** 3 de 3 | **Semana:** 4 de 4 | **Día:** 3 de 5

---

## 🎯 Objetivo del Ejercicio

Este proyecto implementa un sistema automatizado de respuesta a incidentes para pipelines de datos, aplicando conceptos de gestión de incidentes, estrategias de recuperación y mejora continua mediante post-mortems. El ejercicio demuestra la capacidad de diseñar, implementar y simular runbooks de incidentes en entornos de producción de datos.

### Competencias Desarrolladas

1. **Gestión de Incidentes:** Diseño de runbooks automatizados para diferentes tipos de incidentes
2. **Estrategias de Recuperación:** Implementación de lógica de escalación y recuperación automática
3. **Post-Mortems:** Creación de templates para análisis de incidentes y mejora continua
4. **Simulación de Escenarios:** Desarrollo de scripts para simular y validar respuestas a incidentes

---

## 🏗️ Estructura del Proyecto

```
incidentes_recuperacion/
├── README.md                    # Este archivo
├── .gitignore                  # Archivos ignorados por Git
├── ALERT_SYSTEM.md             # Documentación del sistema de alertas (PagerDuty/OpsGenie)
├── RESPONSE_TEAM.md            # Definición del equipo de respuesta con roles claros
├── runbook.py                  # Runbook documentado y accesible
├── simulation.py               # Script de simulación completo
├── post_mortem_example.md      # Ejemplo de post-mortem generado
├── practice.md                 # Enunciado del ejercicio práctico
└── theory.md                   # Fundamentos teóricos
```

---

## 🚀 Cómo Ejecutar el Proyecto

### Requisitos Previos

- Python 3.8 o superior
- Git instalado (para clonar el repositorio)

### Pasos de Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/cristianiglesias/incidentes_recuperacion.git
   cd incidentes_recuperacion
   ```

2. **Ejecutar la simulación completa:**
   ```bash
   python simulation.py
   ```

3. **Ejecutar pruebas individuales:**
   ```python
   # Desde la terminal de Python
   from runbook import IncidentRunbook
   
   # Crear instancia del runbook
   runbook = IncidentRunbook()
   
   # Simular incidente
   context = {'triggered_by': 'monitoring', 'affected_components': ['pipeline']}
   response = runbook.handle_incident('pipeline_down', context)
   print(response)
   ```

### Ejecución Rápida

```bash
# Verificar que el runbook funciona
python -c "from runbook import IncidentRunbook; r = IncidentRunbook(); print(f'✅ Runbook listo con {len(r.incident_types)} tipos de incidentes')"

# Ejecutar demostración completa
python simulation.py
```

---

## 📊 Componentes Principales

### 1. Runbook de Incidentes (`runbook.py`)

Implementa la clase `IncidentRunbook` con:

- **Tipos de Incidentes Definidos:**
  - `pipeline_down`: CRÍTICO - Caída de pipeline de producción
  - `data_quality_degraded`: ALTO - Degradación de calidad de datos
  - `performance_degraded`: MEDIO - Problemas de rendimiento

- **Matriz de Escalación:** Reglas de tiempo/severidad para notificaciones
- **Pasos Automatizados:** Funciones simuladas para cada acción del runbook
- **Verificación de Resolución:** Lógica para determinar si un incidente está resuelto

### 2. Sistema de Simulación (`simulation.py`)

Script completo que demuestra:

- **Respuesta a Incidente Individual:** Manejo de incidente de pipeline caído
- **Múltiples Tipos de Incidentes:** Demostración de los 3 tipos definidos
- **Lógica de Escalación:** Ejemplos de notificaciones basadas en tiempo
- **Template de Post-Mortem:** Generación de documento de análisis
- **Respuestas a Preguntas Teóricas:** Explicaciones basadas en conceptos aprendidos

### 3. Template de Post-Mortem

Función `create_post_mortem_template()` que genera documentos estructurados con:

- Resumen ejecutivo y línea de tiempo
- Análisis de impacto y causa raíz
- Pasos de resolución y lecciones aprendidas
- Items de acción y medidas de prevención

---

## 🧪 Resultados Esperados

### Ejecución de la Simulación

Al ejecutar `python simulation.py`, verás:

1. **Simulación de Respuesta a Incidente:**
   - Detección y clasificación del incidente
   - Ejecución paso a paso del runbook
   - Resultados de cada acción con estado ✅/❌

2. **Demostración de Múltiples Incidentes:**
   - Procesamiento de los 3 tipos de incidentes
   - Tiempos de respuesta y estados de resolución

3. **Lógica de Escalación:**
   - Matriz de escalación configurada
   - Ejemplos prácticos de notificaciones basadas en tiempo

4. **Post-Mortem de Ejemplo:**
   - Documento completo generado automáticamente
   - Guardado en `post_mortem_example.md`

5. **Respuestas Teóricas:**
   - Explicación de incidentes críticos vs. no críticos
   - Criterios para escalación de incidentes

---

## 🧠 Conceptos Aplicados

### Gestión de Incidentes
- Clasificación por severidad (CRITICAL, HIGH, MEDIUM)
- Definición de SLAs y tiempos de respuesta
- Runbooks documentados y accesibles

### Estrategias de Recuperación
- Recuperación automática vs. intervención manual
- Matrices de escalación basadas en tiempo
- Verificación de resolución automatizada

### Mejora Continua
- Post-mortems estructurados (Facts, Timeline, Root Cause, Impact, Lessons)
- Análisis de causa raíz
- Prevención de incidentes recurrentes

---

## 🔧 Requisitos del Sistema

### Dependencias de Python
```txt
Python 3.8+
No se requieren librerías externas (usa solo módulos estándar)
```

### Arquitectura Recomendada
- Sistema de alertas configurado (PagerDuty, OpsGenie, etc.)
- Equipo de respuesta definido con roles claros
- Monitoreo de métricas de pipelines
- Logging centralizado para trazabilidad

---

## 📈 Aprendizajes Clave

1. **Priorización de Incidentes:** Diferenciar entre incidentes que requieren respuesta inmediata vs. aquellos que pueden esperar
2. **Toma de Decisiones:** Criterios claros para escalación basados en tiempo, severidad e impacto
3. **Automatización:** Diseño de runbooks que balancean automatización e intervención humana
4. **Cultura de Mejora:** Uso de post-mortems como herramienta de aprendizaje organizacional

---

## 👨‍🏫 Contexto Educativo

Este ejercicio forma parte del **curso de Ciencia de Datos de Talent Ops**, específicamente del último módulo (3/3) donde se integran conocimientos de:

- **Ingeniería de Datos:** Pipelines, ETL, calidad de datos
- **Operaciones:** Gestión de incidentes, monitorización, SLA
- **Desarrollo de Software:** Patrones de diseño, testing, documentación

Como docente y profesional en el área, este proyecto refleja la aplicación de conceptos teóricos en escenarios prácticos reales, preparando a los estudiantes para enfrentar desafíos en entornos de producción de datos.

---

## 📞 Contacto y Contribuciones

**Autor:** Cristian Iglesias  
**GitHub:** [cristianiglesias](https://github.com/cristianiglesias)  
**Rol:** Técnico en Producción de Software | Desarrollador Full Stack Python | Docente UC Temuco

Este proyecto está abierto a mejoras y contribuciones. Si encuentras algún issue o tienes sugerencias, por favor crea un PR o abre un issue en el repositorio.

---

## 📄 Licencia

Este proyecto es educativo y puede ser utilizado como referencia para fines de aprendizaje. Se recomienda citar al autor si se utiliza en otros contextos.

---
*Última actualización: Enero 2026*  
*Curso: Ciencia de Datos - Talent Ops | Módulo 3 | Semana 4 | Día 3*