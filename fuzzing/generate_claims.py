import random
import json
import datetime
import os

# Configuración
OUTPUT_FILE = "data/synthetic_claims.jsonl"
NUM_SAMPLES = 100

# Datos para generación
nombres = [
    "Juan", "Maria", "Pedro", "Ana", "Luis", "Sofia", "Carlos", "Lucia", 
    "Diego", "Valentina", "Miguel", "Camila", "Javier", "Paula", "Fernando", "Martina"
]
marcas = [
    "Toyota Corolla", "Ford Fiesta", "Honda Civic", "Chevrolet Onix", "Fiat Cronos", "VW Gol", "Peugeot 208",
    "Renault Sandero", "Toyota Hilux", "Ford Ranger", "Nissan Versa", "Jeep Renegade", "Chevrolet Cruze"
]
colores = ["rojo", "azul", "blanco", "negro", "gris", "plateado", "verde", "bordo", "dorado", "azul oscuro"]
calles = [
    "Av. Libertador", "Calle 9 de Julio", "Ruta 2", "Av. Corrientes", "Calle San Martín",
    "Av. Cabildo", "Av. Santa Fe", "Autopista Panamericana", "Av. General Paz", "Calle Florida"
]
acciones = [
    "me chocó de atrás", "me rayó el costado", "se cruzó en rojo", "frenó de golpe", "me rompió el espejo",
    "me encerró", "no respetó la prioridad", "dio marcha atrás sin mirar", "abrió la puerta sin mirar", "cambió de carril bruscamente"
]
consecuencias = [
    "tengo el paragolpes roto", "la puerta no abre", "solo fue un susto", "el faro está destruido", "necesito grúa",
    "el baúl no cierra", "tengo un bollo en la puerta", "se rompió la óptica", "el radiador pierde agua", "tengo el espejo colgando"
]

def generar_fecha_reciente():
    dias_atras = random.randint(0, 30)
    fecha = datetime.date.today() - datetime.timedelta(days=dias_atras)
    return fecha.strftime("%Y-%m-%d")

def introducir_ruido(texto):
    # Simula errores de tipeo o redacción informal
    if random.random() < 0.3:
        texto = texto.lower() # Todo minúsculas
    if random.random() < 0.2:
        texto = texto.replace(".", "") # Sin puntos
    if random.random() < 0.1:
        texto = texto.replace(" de ", " d ") # Abreviaciones chat
    return texto

def generar_reclamo():
    nombre = random.choice(nombres)
    mi_auto = random.choice(marcas)
    otro_auto = random.choice(marcas)
    calle = random.choice(calles)
    accion = random.choice(acciones)
    consecuencia = random.choice(consecuencias)
    fecha = generar_fecha_reciente()
    
    # Plantillas de redacción
    plantillas = [
        f"Hola, soy {nombre}. El {fecha} iba por {calle} con mi {mi_auto} y un {otro_auto} {accion}. {consecuencia}.",
        f"Siniestro ocurrido el {fecha}. Lugar: {calle}. Vehículo asegurado: {mi_auto}. Tercero: {otro_auto}. Descripción: {accion}.",
        f"Tuve un accidente en {calle} ayer. Un {otro_auto} {accion} a mi {mi_auto}. {consecuencia}.",
        f"{fecha}: Choque en {calle}. {mi_auto} vs {otro_auto}. {accion}."
    ]
    
    texto_base = random.choice(plantillas)
    texto_final = introducir_ruido(texto_base)
    
    return {
        "text": texto_final,
        "metadata": {
            "fecha": fecha,
            "lugar": calle,
            "vehiculo_asegurado": mi_auto,
            "vehiculo_tercero": otro_auto,
            "tipo_incidente": accion
        }
    }

def main():
    print(f"Generando {NUM_SAMPLES} reclamos sintéticos con Fuzzing...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for _ in range(NUM_SAMPLES):
            reclamo = generar_reclamo()
            f.write(json.dumps(reclamo, ensure_ascii=False) + "\n")
    print(f"Datos guardados en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
