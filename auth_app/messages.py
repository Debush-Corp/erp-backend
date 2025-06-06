# auth_app/messages.py
MESSAGES = {
    'LoginView': {
        200: 'Inicio de sesión exitoso',
        400: 'Credenciales inválidas o datos faltantes',
        401: 'No autorizado para iniciar sesión',
    },
    'RefreshView': {
        200: 'Token de acceso renovado exitosamente',
        400: 'Token de refresco inválido o faltante',
        401: 'Token de refresco expirado o no autorizado',
    },
    'LogoutView': {
        205: 'Cierre de sesión exitoso',
        400: 'Token de refresco inválido o no proporcionado',
        401: 'Debes estar autenticado para cerrar sesión',
    },
    'MeView': {
        200: 'Datos del usuario obtenidos exitosamente',
        401: 'Debes estar autenticado para ver tus datos',
    },
}