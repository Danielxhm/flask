# routes/alquileresdb.py
import uuid # Para generar IDs únicos para los alquileres

alquileres_db = []

def guardar_alquiler(alquiler_data):
    global alquileres_db
    # Añadir un ID único y un estado de aprobación inicial
    alquiler_data['id_alquiler'] = str(uuid.uuid4()) # ID único para cada alquiler
    alquiler_data['estado_aprobacion'] = 'pendiente' # Estados: pendiente, aprobado, rechazado
    alquileres_db.append(alquiler_data)
    print(f"DEBUG ALQUILERESDB (guardar): Alquiler guardado: {alquiler_data}")

def obtener_todos_los_alquileres():
    global alquileres_db
    print(f"DEBUG ALQUILERESDB (obtener_todos): Devolviendo alquileres: {alquileres_db}")
    return alquileres_db

def obtener_alquiler_por_id(id_alquiler):
    global alquileres_db
    for alq in alquileres_db:
        if alq.get('id_alquiler') == id_alquiler:
            return alq
    return None

def actualizar_estado_aprobacion_alquiler(id_alquiler, nuevo_estado):
    global alquileres_db
    alquiler_encontrado = False
    for alq in alquileres_db:
        if alq.get('id_alquiler') == id_alquiler:
            alq['estado_aprobacion'] = nuevo_estado
            print(f"DEBUG ALQUILERESDB (actualizar_estado): Alquiler ID {id_alquiler} actualizado a '{nuevo_estado}'. Alquiler: {alq}")
            alquiler_encontrado = True
            return True
    if not alquiler_encontrado:
        print(f"ERROR ALQUILERESDB (actualizar_estado): Alquiler ID {id_alquiler} no encontrado.")
    return False


def eliminar_alquileres_por_email(email):
    global alquileres_db
    alquileres_original_len = len(alquileres_db)
    alquileres_db = [alq for alq in alquileres_db if alq.get('email') != email]
    if len(alquileres_db) < alquileres_original_len:
        print(f"Alquileres eliminados para el email: {email}. Antes: {alquileres_original_len}, Ahora: {len(alquileres_db)}")
    else:
        print(f"No se encontraron alquileres para eliminar con el email: {email}")