from routes.alquileresdb import eliminar_alquileres_por_email
# Variable global que guarda los usuarios
usuarios = {
    'admin': {
        'password': 'admin123',
        'nombre': 'Administrador',
        'email': 'admin@motorent.com',
        'rol': 'SuperAdmin'
    }
}

def obtener_usuarios():
    global usuarios
    return usuarios

def agregar_usuario(username, datos):
    global usuarios
    if username in usuarios:
        print(f"Advertencia: El usuario {username} ya existe. Sobrescribiendo datos.")
    usuarios[username] = datos
    print(f"Usuarios actualizados después de agregar/actualizar a {username}: {usuarios}")

def eliminar_usuario(username):
    global usuarios
    if username in usuarios:
        if username == 'admin':
            return False, "No se puede eliminar al usuario administrador."

        # Obtener email antes de eliminar
        email = usuarios[username].get('email')

        # Eliminar usuario
        del usuarios[username]
        print(f"Usuario {username} eliminado. Usuarios actualizados: {usuarios}")

        # Eliminar alquileres asociados
        if email:
            eliminar_alquileres_por_email(email)

        return True, f"Usuario {username} eliminado correctamente."
    return False, f"Usuario {username} no encontrado."


def cambiar_password_confirmando(username, password_actual, nueva_password):
    global usuarios
    if username in usuarios:
        password_guardada = usuarios[username].get('password')

        if password_guardada != password_actual:
            return False, "La contraseña actual ingresada es incorrecta."

        usuarios[username]['password'] = nueva_password
        print(f"Contraseña actualizada para {username}.")

        # Opcional: guardar en archivo si aplica
        # guardar_usuarios(usuarios)

        return True, "Contraseña actualizada correctamente."

    return False, "Usuario no encontrado."
