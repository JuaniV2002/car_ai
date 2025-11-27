import json
from collections import Counter
import statistics
import difflib
import re

INPUT_FILE = 'data/processed_claims.jsonl'

def normalize(text):
    """Normalización básica: minúsculas, elimina puntuación (mantiene espacios).

    Maneja cadenas y diccionarios (aplana valores del dict).
    """
    if not text:
        return ""

    if isinstance(text, dict):
        parts = [str(v) for v in text.values() if v]
        text = " ".join(parts)

    # Minúsculas y eliminar puntuación (mantener espacios)
    text = str(text).lower().strip()
    text = re.sub(r"[\.,;:\'\"\(\)\[\]\\/\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text):
    """Divide el texto normalizado en tokens (palabras)."""
    if not text:
        return []
    return [t for t in text.split() if t]


def normalize_vehicle(text):
    """Normaliza cadenas de vehículos para que 'ford fiesta' == 'fiesta ford'.

    Retorna una cadena canónica ordenando los tokens alfabéticamente.
    """
    norm = normalize(text)
    tokens = tokenize(norm)
    # Eliminar palabras de relleno comunes
    fillers = {"the", "a", "an", "mi", "my", "un", "una", "el", "la"}
    tokens = [t for t in tokens if t not in fillers]
    tokens_sorted = sorted(tokens)
    return " ".join(tokens_sorted)


def similarity_ratio(a, b):
    """Retorna el ratio de similitud usando difflib.SequenceMatcher."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def token_overlap_ratio(a, b):
    """Solapamiento de tokens: intersección / unión."""
    ta = set(tokenize(normalize(a)))
    tb = set(tokenize(normalize(b)))
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    inter = ta & tb
    union = ta | tb
    return len(inter) / len(union)


def is_vehicle_match(gt_val, ext_val):
    """Coincidencia semántica heurística para vehículos.

    Pasos:
    - Canonicaliza ordenando tokens y compara exactamente
    - Si no, usa solapamiento de tokens o ratio de similitud
    """
    gt_norm = normalize_vehicle(gt_val)
    ext_norm = normalize_vehicle(ext_val)
    if not gt_norm and not ext_norm:
        return True
    if gt_norm == ext_norm and gt_norm:
        return True

    # Umbral de solapamiento de tokens
    overlap = token_overlap_ratio(gt_val, ext_val)
    if overlap >= 0.6:
        return True

    # Fallback a similitud de secuencia
    seq = similarity_ratio(str(gt_val).lower() if gt_val else "", str(ext_val).lower() if ext_val else "")
    if seq >= 0.7:
        return True

    return False


def is_description_match(gt_val, ext_val):
    """Verificación semántica para descripciones cortas.

    Usa solapamiento de tokens y similitud de secuencia con umbrales conservadores.
    """
    if not gt_val and not ext_val:
        return True
    overlap = token_overlap_ratio(gt_val, ext_val)
    if overlap >= 0.5:
        return True
    seq = similarity_ratio(normalize(gt_val), normalize(ext_val))
    return seq >= 0.6

def calculate_metrics():
    total_claims = 0
    field_matches = Counter()
    field_totals = Counter()
    processing_times = []
    swaps = 0
    
    print(f"{'ID':<5} | {'Campo':<20} | {'Valor Real':<30} | {'Extraído':<30} | {'Resultado'}")
    print("-" * 110)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            record = json.loads(line)
            total_claims += 1
            processing_times.append(record.get('processing_time', 0))
            
            gt = record['ground_truth']
            ext = record['extracted_data']
            
            # Mapeo de campos a comparar (Clave Extraída -> Clave Real)
            comparisons = [
                ('fecha', 'fecha'),
                ('ubicacion', 'lugar'),
                ('vehiculo_asegurado', 'vehiculo_asegurado'),
                ('vehiculo_tercero', 'vehiculo_tercero'),
                ('responsabilidad_aparente', 'responsabilidad')
            ]
            
            claim_has_swap = False
            
            for ext_key, gt_key in comparisons:
                gt_val = gt.get(gt_key)
                ext_val = ext.get(ext_key)

                field_totals[ext_key] += 1

                norm_gt = normalize(gt_val)
                norm_ext = normalize(ext_val)

                # Lógica de coincidencia (mejorada para coincidencia semántica)
                match = False
                is_swap = False

                # Vehículos: usar coincidencia semántica
                if ext_key in ['vehiculo_asegurado', 'vehiculo_tercero']:
                    if is_vehicle_match(gt_val, ext_val):
                        match = True
                    else:
                        # Verificar si coincide con el otro vehículo (intercambio)
                        other_key = 'vehiculo_tercero' if ext_key == 'vehiculo_asegurado' else 'vehiculo_asegurado'
                        other_gt_val = gt.get(other_key)
                        if is_vehicle_match(other_gt_val, ext_val):
                            is_swap = True
                            claim_has_swap = True
                else:
                    # Para otros campos: fecha/ubicacion/responsabilidad - verificación difusa original
                    if norm_gt == norm_ext:
                        match = True
                    elif norm_gt and norm_ext and (norm_gt in norm_ext or norm_ext in norm_gt):
                        match = True
                    else:
                        # Manejo especial para descripcion_breve si está presente
                        if ext_key == 'descripcion_breve':
                            if is_description_match(gt_val, ext_val):
                                match = True

                # Actualizar estadísticas
                if match:
                    field_matches[ext_key] += 1
                else:
                    status = "INTERCAMBIADO" if is_swap else "NO COINCIDE"
                    # Truncar cadenas largas para visualización
                    d_gt = (str(gt_val)[:28] + '..') if len(str(gt_val)) > 28 else str(gt_val)
                    d_ext = (str(ext_val)[:28] + '..') if len(str(ext_val)) > 28 else str(ext_val)
                    print(f"{record['id']:<5} | {ext_key:<20} | {d_gt:<30} | {d_ext:<30} | {status}")

            if claim_has_swap:
                swaps += 1

    print("-" * 110)
    print("\n=== REPORTE DE VALIDACIÓN ===")
    print(f"Total de Reclamos Procesados: {total_claims}")
    print(f"Tiempo Promedio de Procesamiento: {statistics.mean(processing_times):.2f}s")

    print("\nPrecisión por Campo:")
    for field in ['fecha', 'ubicacion', 'vehiculo_asegurado', 'vehiculo_tercero', 'responsabilidad_aparente']:
        total = field_totals[field]
        matches = field_matches[field]
        accuracy = (matches / total * 100) if total > 0 else 0
        print(f"  - {field:<25}: {accuracy:>6.1f}%  ({matches}/{total})")

    print(f"\nIntercambio de Roles (Vehículos): {swaps} reclamos ({swaps/total_claims*100:.1f}%)")
    print("  (El modelo confundió quién era el asegurado vs el tercero)")

if __name__ == "__main__":
    calculate_metrics()
