# Extracción de Datos de Siniestros - Reporte de Desempeño

## Configuración del Experimento
- **Modelo:** Llama 3.2 (vía Ollama)
- **Dataset:** 50 Reclamos Sintéticos generados vía Fuzzing
- **Nivel de Ruido:** Alto (errores de tipeo, jerga, falta de puntuación)
- **Hardware:** Ejecución Local (macOS)

## 📊 Resultados Cuantitativos

| Campo | Precisión | Notas |
| :--- | :--- | :--- |
| **Ubicación** | **100.0%** | Extracción perfecta a pesar del ruido (ej: "av. libertador" vs "Av Libertador"). |
| **Vehículos** | **98.0%** | Alta precisión identificando Marca/Modelo. |
| **Asignación de Roles** | **98.0%** | Solo 2% de error distinguiendo Asegurado vs. Tercero. |
| **Fecha** | **76.0%** | Precisión más baja debido a fechas relativas (ej: "ayer"). |

**Tiempo Promedio de Procesamiento:** 7.99 segundos por reclamo.

## 🔍 Análisis de Errores

### 1. El Problema del "Contexto" (Alucinación de Fechas)
La mayoría de los errores ocurrieron en el campo `fecha`.
- **Entrada:** "Tuve un accidente... ayer".
- **Problema:** No se le proporcionó la "Fecha Actual" al modelo en el prompt del sistema.
- **Resultado:** El modelo alucinó una fecha aleatoria (ej: `2024-03-18`) o devolvió `null`.
- **Solución:** Inyectar `Fecha Actual: {datetime.now()}` en el System Prompt.

### 2. Intercambio de Roles
En 1 caso (Reclamo #1), el modelo intercambió los vehículos:
- **Texto:** "Un Ford Fiesta me rayó el costado a mi Honda Civic"
- **Realidad:** Asegurado=Honda Civic, Tercero=Ford Fiesta.
- **Extraído:** Asegurado=Ford Fiesta, Tercero=Honda Civic.
- **Causa:** Estructuras de oraciones complejas ("A hizo X a B") a veces pueden confundir a modelos más pequeños (3B parámetros).

## ✅ Conclusión
El sistema demuestra **alta viabilidad** para automatizar el procesamiento de reclamos. Las entidades principales (Dónde, Quién, Qué) se extraen con >98% de precisión. El problema de la fecha es una corrección de ingeniería trivial (inyección de contexto), no una limitación de capacidad del modelo.
