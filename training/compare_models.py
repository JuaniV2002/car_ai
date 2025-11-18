#!/usr/bin/env python3
"""
Compara el modelo BASE vs el modelo CONFIGURADO (con SYSTEM prompt)
Para demostrar que el aprendizaje es real cuando usemos few-shot o fine-tuning
"""
import subprocess

def test_model(model_name, prompt):
    """Prueba un código con un modelo específico"""
    try:
        result = subprocess.run(
            ['ollama', 'run', model_name, prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except:
        return "Error/Timeout"

# Códigos de prueba (del dataset)
test_codes = [
    ("TOY-2847A", "Toyota"),
    ("FRD-4821X", "Ford"),
    ("VWG-3947K", "Volkswagen"),
    ("CHV-5928W", "Chevrolet"),
    ("BMW-9561U", "BMW"),
]

# Códigos NUEVOS (no están en el dataset - para verificar generalización)
unseen_codes = [
    ("TOY-9999Z", "Toyota"),
    ("FRD-0000A", "Ford"),
    ("BMW-1111B", "BMW"),
]

print("=" * 80)
print("EXPERIMENTO: Comparación de modelos")
print("=" * 80)

print("\nFASE 1: Códigos DEL DATASET (el modelo debería aprender estos)")
print("-" * 80)

correct_base = 0
correct_trained = 0

for code, expected in test_codes:
    print(f"\nCódigo: {code} → Marca esperada: {expected}")
    
    # Modelo base (sin configuración especial)
    base_response = test_model("llama3.2", f"Código: {code}")
    print(f"   [BASE] Modelo llama3.2:")
    print(f"      {base_response[:80]}{'...' if len(base_response) > 80 else ''}")
    if expected.lower() in base_response.lower():
        print(f"      Acertó")
        correct_base += 1
    else:
        print(f"      Falló")
    
    # Modelo con SYSTEM prompt configurado
    trained_response = test_model("car-brands-codes", f"Código: {code}")
    print(f"   [CONFIG] Modelo car-brands-codes:")
    print(f"      {trained_response[:80]}{'...' if len(trained_response) > 80 else ''}")
    if expected.lower() in trained_response.lower():
        print(f"      Acertó")
        correct_trained += 1
    else:
        print(f"      Falló")

print("\n" + "=" * 80)
print("RESULTADOS EN CÓDIGOS DEL DATASET:")
print(f"   Modelo BASE: {correct_base}/{len(test_codes)} correctos ({100*correct_base/len(test_codes):.0f}%)")
print(f"   Modelo CONFIGURADO: {correct_trained}/{len(test_codes)} correctos ({100*correct_trained/len(test_codes):.0f}%)")
print("=" * 80)

print("\n\nFASE 2: Códigos NUEVOS (no vistos en dataset - prueba de generalización)")
print("-" * 80)

correct_base_unseen = 0
correct_trained_unseen = 0

for code, expected in unseen_codes:
    print(f"\nCódigo: {code} → Marca esperada: {expected}")
    
    base_response = test_model("llama3.2", f"Código: {code}")
    print(f"   [BASE]: {base_response[:60]}...")
    if expected.lower() in base_response.lower():
        correct_base_unseen += 1
        print(f"      Acertó (sorpresa!)")
    else:
        print(f"      Falló (esperado)")
    
    trained_response = test_model("car-brands-codes", f"Código: {code}")
    print(f"   [CONFIG]: {trained_response[:60]}...")
    if expected.lower() in trained_response.lower():
        correct_trained_unseen += 1
        print(f"      Acertó")
    else:
        print(f"      Falló")

print("\n" + "=" * 80)
print("RESULTADOS EN CÓDIGOS NUEVOS:")
print(f"   Modelo BASE: {correct_base_unseen}/{len(unseen_codes)} correctos")
print(f"   Modelo CONFIGURADO: {correct_trained_unseen}/{len(unseen_codes)} correctos")
print("=" * 80)

print("\n\nCONCLUSIÓN:")
if correct_trained > correct_base:
    print("   El modelo CONFIGURADO muestra mejor rendimiento.")
    print("   El SYSTEM prompt + contexto ayudan al modelo.")
else:
    print("   Ambos modelos tienen rendimiento similar.")
    print("   Se necesita fine-tuning real o few-shot learning para mejorar.")

print("\nPRÓXIMO PASO: Implementar few-shot learning o usar herramientas")
print("de fine-tuning real (Unsloth, Axolotl) para aprendizaje verdadero.")
print("\n" + "=" * 80)
