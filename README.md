# Extractor de Datos de Siniestros con IA

Este proyecto implementa un sistema inteligente para extraer información estructurada a partir de descripciones de accidentes de tránsito no estructuradas (texto libre). Combina técnicas de **Fuzzing** para la generación de datos sintéticos y **LLMs (Modelos de Lenguaje Grande)** para el procesamiento de información.

## 🎯 Objetivo

Demostrar la capacidad de los LLMs para "limpiar" y estructurar datos ruidosos del mundo real, una tarea que sería imposible con expresiones regulares (Regex) o SQL tradicional.

El sistema toma descripciones informales como:
> *"Tuve un accidente en av libertador ayer un ford fiesta me rayó el costado a mi honda civic necesito grúa"*

Y las convierte en JSON estructurado:
```json
{
  "fecha": "2024-03-18",
  "ubicacion": "Av. Libertador",
  "vehiculo_asegurado": "Honda Civic",
  "vehiculo_tercero": "Ford Fiesta",
  "responsabilidad_aparente": "tercero"
}
```

## 🏗️ Arquitectura del Proyecto

El proyecto consta de tres módulos principales:

1.  **Generación de Datos (Fuzzing):**
    *   Script: `fuzzing/generate_claims.py`
    *   Genera reclamos sintéticos inyectando "ruido" intencional: errores de ortografía, falta de puntuación, jerga ("me chocó de atrás"), y formatos de fecha variados.
    *   Simula la variabilidad de datos reales ingresados por usuarios.

2.  **Procesamiento con IA:**
    *   Script: `src/process_claims.py`
    *   Utiliza **Ollama** con el modelo **Llama 3.2**.
    *   Implementa un *System Prompt* robusto diseñado para inferir roles (quién chocó a quién) y normalizar entidades.

3.  **Validación y Métricas:**
    *   Script: `src/validate_results.py`
    *   Compara la salida del LLM contra el "Ground Truth" (la verdad absoluta generada por el fuzzer).
    *   Calcula precisión por campo y detecta errores lógicos (como intercambiar vehículos).

## 🚀 Cómo Ejecutar

### Prerrequisitos
- Python 3
- Ollama instalado y ejecutándose (`ollama serve`)
- Modelo Llama 3.2 (`ollama pull llama3.2`)

### Pasos

1.  **Generar Datos de Prueba:**
    ```bash
    python3 fuzzing/generate_claims.py
    ```
    *Esto creará `data/synthetic_claims.jsonl` con 50 casos de prueba.*

2.  **Ejecutar el Extractor:**
    ```bash
    python3 src/process_claims.py
    ```
    *Procesará los reclamos y guardará los resultados en `data/processed_claims.jsonl`.*

3.  **Ver Resultados y Métricas:**
    ```bash
    python3 src/validate_results.py
    ```
    *Mostrará una tabla comparativa y el porcentaje de precisión.*

## 📊 Resultados Obtenidos

En pruebas locales con Llama 3.2 (3B parámetros), el sistema logró:
- **100%** de precisión en detección de Ubicación.
- **98%** de precisión en identificación de Vehículos.
- **98%** de precisión en asignación de Responsabilidad.

*Ver el reporte completo en `metrics_report.md`.*

## 🛠️ Tecnologías Utilizadas

- **Python 3**: Lenguaje principal.
- **Ollama**: Runtime local para LLMs.
- **Llama 3.2**: Modelo de lenguaje optimizado para instrucciones.
- **JSONL**: Formato de datos para procesamiento eficiente.

---
*Proyecto desarrollado para la materia de Inteligencia Artificial.*