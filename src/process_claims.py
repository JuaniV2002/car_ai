import json
import urllib.request
import urllib.error
import time
import random
from datetime import datetime
import validate_results

# Configuration
INPUT_FILE = 'data/synthetic_claims.jsonl'
OUTPUT_FILE = 'data/processed_claims.jsonl'
MODEL_NAME = 'llama3.2'
API_URL = 'http://localhost:11434/api/chat'

SYSTEM_PROMPT = """
Eres un asistente experto en seguros y procesamiento de datos. Tu tarea es extraer información estructurada de descripciones de siniestros de autos que pueden contener errores ortográficos, jerga o texto informal.

Debes extraer la siguiente información en formato JSON estricto:
{
    "fecha": "YYYY-MM-DD" o null,
    "hora": "HH:MM" o null,
    "ubicacion": "calle, ciudad o referencia geográfica",
    "vehiculo_asegurado": "Marca y Modelo",
    "vehiculo_tercero": "Marca y Modelo" o null,
    "descripcion_breve": "Resumen del accidente",
    "responsabilidad_aparente": "asegurado", "tercero" o "indeterminado"
}

Reglas:
1. Si no encuentras un dato, usa null.
2. Corrige errores ortográficos en los nombres de calles o marcas si es obvio.
3. Infiere la responsabilidad basándote en la descripción (ej: "me chocaron de atrás" implica responsabilidad del tercero).
4. Responde ÚNICAMENTE con el JSON, sin texto adicional.
"""

def extract_info(text):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "stream": False,
        "format": "json"
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(API_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['message']['content']
    except urllib.error.URLError as e:
        print(f"Error conectando con Ollama: {e}")
        return None

def main():
    print(f"Iniciando procesamiento de {INPUT_FILE}...")
    
    processed_count = 0
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f_in:
        all_lines = f_in.readlines()

    selected_lines = random.sample(all_lines, min(5, len(all_lines)))
    print(f"Procesando muestra aleatoria de {len(selected_lines)} reclamos...")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        
        for i, line in enumerate(selected_lines, 1):
            record = json.loads(line)
            claim_text = record['text']
            ground_truth = record['metadata']
            
            print(f"\nProcesando Reclamo #{i}...")
            print(f"Entrada: {claim_text}")
            
            start_time = time.time()
            extracted_json_str = extract_info(claim_text)
            duration = time.time() - start_time
            
            if extracted_json_str:
                try:
                    extracted_data = json.loads(extracted_json_str)
                    
                    # Crear registro de resultado
                    result = {
                        "id": i,
                        "original_text": claim_text,
                        "ground_truth": ground_truth,
                        "extracted_data": extracted_data,
                        "processing_time": round(duration, 2)
                    }
                    
                    f_out.write(json.dumps(result, ensure_ascii=False) + '\n')
                    print(f"¡Éxito! (Tiempo: {duration:.2f}s)")
                    print(f"Extraído: {json.dumps(extracted_data, ensure_ascii=False, indent=2)}")
                    processed_count += 1
                    
                except json.JSONDecodeError:
                    print(f"Error al analizar respuesta JSON: {extracted_json_str}")
            else:
                print("Error al obtener respuesta del modelo.")

    print(f"\nProcesamiento completo. {processed_count} reclamos procesados.")
    print(f"Resultados guardados en {OUTPUT_FILE}")
    
    print("\n" + "="*50 + "\n")
    validate_results.calculate_metrics()

if __name__ == "__main__":
    main()
