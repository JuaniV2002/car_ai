# Proyecto Final - Inteligencia Artificial

Identificador de marcas de automóviles usando códigos alfanuméricos inventados. El objetivo es demostrar aprendizaje real en un LLM mediante few-shot learning.

## Objetivo

Demostrar que un LLM puede aprender información completamente nueva (códigos que nunca vio antes) usando:
- Few-shot learning (ejemplos en el prompt)
- System prompts configurados
- Prompt engineering

## Prueba de Aprendizaje

### Sin entrenamiento (modelo base):
```bash
echo "Código: TOY-2847A" | ollama run llama3.2
# Respuesta: "No puedo identificar el código TOY-2847A..."
# Precisión: 0%
```

### Con few-shot learning:
```bash
python3 training/few_shot_learning.py
# Precisión: 67% en códigos del dataset
# Precisión: 50% en códigos nuevos (generalización)
```

El modelo aprende códigos que nunca existieron en su entrenamiento original.

## Estructura del Proyecto

```
car_ai/
├── dataset/
│   ├── dataset_codes.jsonl         # Dataset con códigos INVENTADOS
├── training/
│   ├── training_data_codes.jsonl   # Dataset convertido para Ollama
│   ├── convert_dataset.py          # Convertir formato
│   ├── few_shot_learning.py        # Experimento principal con few-shot learning
│   ├── compare_models.py           # Comparación antes/después
│   ├── verify_base_model.py        # Verificar que códigos son nuevos
│   └── visualize_results.py        # Visualización de resultados
├── Modelfile_codes                 # Config para códigos inventados
└── README.md
```

## Uso

### Experimento 1: Verificar que el modelo NO conoce los códigos
```bash
python3 training/verify_base_model.py
```

### Experimento 2: Comparar modelo base vs configurado
```bash
python3 training/compare_models.py
```

### Experimento 3: Few-Shot Learning (experimento principal)
```bash
python3 training/few_shot_learning.py
```

Este experimento demuestra que:
- El modelo aprende códigos completamente nuevos
- Generaliza a códigos no vistos (detecta patrones)
- Mejora de 0% → 67% de precisión

## Ejemplos

### Verificación del modelo base:
```bash
echo "Código: TOY-2847A" | ollama run llama3.2
# "No puedo identificar este código"
```

### Con few-shot learning:
```bash
python3 training/few_shot_learning.py
# El modelo aprende que TOY-2847A → Toyota
```

## Dataset

### Códigos Inventados (`dataset_codes.jsonl`)
- Total: 100 ejemplos
- Códigos: TOY-2847A, FRD-4821X, VWG-3947K, etc.
- El modelo nunca vio estos códigos en su entrenamiento
- Permite demostrar aprendizaje real

#### Formato de códigos:
```
TOY-XXXX → Toyota
FRD-XXXX → Ford
VWG-XXXX → Volkswagen
CHV-XXXX → Chevrolet
RNT-XXXX → Renault
FIA-XXXX → Fiat
PGT-XXXX → Peugeot
HND-XXXX → Honda
BMW-XXXX → BMW
MBZ-XXXX → Mercedes-Benz
```

## Tecnologías

- LLM: llama3.2 (3B parámetros)
- Framework: Ollama
- Técnicas:
  - Few-shot learning
  - Prompt engineering
  - System prompts
  - In-context learning
- Lenguaje: Python 3

## Resultados

| Método | Precisión en Dataset | Precisión en Nuevos | Aprendizaje Real |
|--------|---------------------|---------------------|------------------|
| Modelo base | 0% | 0% | No |
| System prompt | 60% | 10% | Parcial |
| Few-shot learning | 67% | 50% | Sí |

Few-shot learning demuestra que el modelo puede aprender información completamente nueva con solo ver ejemplos.

## Requisitos

- Ollama instalado
- Python 3.x
- Modelo llama3.2 descargado (`ollama pull llama3.2`)

## Notas Técnicas

- Temperature: 0.3 (respuestas más deterministas)
- Top_p: 0.9
- Max tokens: 20 (respuestas cortas)
- El modelo está optimizado para respuestas concisas de una sola palabra (la marca)

## Metodología

### Problema:
¿Cómo demostrar que el modelo realmente aprende algo nuevo y no solo usa conocimiento previo?

### Solución:
1. Crear códigos alfanuméricos que no existen en el mundo real
2. Verificar que el modelo base no los conoce (0% precisión)
3. Aplicar few-shot learning con 20 ejemplos
4. Demostrar mejora: 0% → 67%
5. El modelo generaliza a códigos nuevos (50%)

### Contribución:
- Demuestra comprensión de in-context learning
- Aplica técnicas de prompt engineering
- Mide el aprendizaje de forma cuantitativa
- Documenta experimentos con metodología científica
