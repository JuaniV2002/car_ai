#!/usr/bin/env python3
"""
Convierte el dataset de formato simple a formato Ollama para fine-tuning
"""
import json

import sys


INPUT_FILE = "./dataset/dataset.jsonl"
OUTPUT_FILE = "./training/training_data.jsonl"

def convert_to_ollama_format():
    """Convierte cada entrada al formato de chat que Ollama espera"""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f_in:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
            for line in f_in:
                line = line.strip()
                if not line:  # Saltar líneas vacías
                    continue
                data = json.loads(line)
                
                # Formato de chat para Ollama
                ollama_entry = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "Eres un sistema de identificación de marcas de automóviles por código. Dado un código alfanumérico, debes responder únicamente con el nombre de la marca correspondiente."
                        },
                        {
                            "role": "user",
                            "content": data["prompt"]
                        },
                        {
                            "role": "assistant",
                            "content": data["completion"]
                        }
                    ]
                }
                
                f_out.write(json.dumps(ollama_entry, ensure_ascii=False) + '\n')
    
    print(f"Dataset convertido: {OUTPUT_FILE}")
    
    # Mostrar un ejemplo
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        print("\nEjemplo de entrada convertida:")
        print(json.dumps(json.loads(first_line), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    convert_to_ollama_format()
