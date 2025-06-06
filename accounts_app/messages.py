MESSAGES = {
    'UserListCreateView': {
        200: 'Lista de usuarios obtenida exitosamente',
        201: 'Usuario creado exitosamente',
        400: 'Datos inválidos para listar o crear usuario',
        403: 'No tienes permiso para acceder a la lista de usuarios o crear usuarios',
    },
    'UserDetailView': {
        200: 'Detalles del usuario obtenidos exitosamente',
        204: 'Usuario eliminado exitosamente',
        400: 'Datos inválidos para actualizar usuario',
        403: 'No tienes permiso para modificar o eliminar este usuario',
        404: 'Usuario no encontrado',
    },
    'GroupListView': {
        200: 'Lista de grupos obtenida exitosamente',
        403: 'No tienes permiso para ver la lista de grupos',
    },
    'GroupDetailView': {
        200: 'Detalles del grupo obtenidos exitosamente',
        204: 'Grupo eliminado exitosamente',
        400: 'Datos inválidos para actualizar grupo',
        403: 'No tienes permiso para modificar o eliminar este grupo',
        404: 'Grupo no encontrado',
    },
    'GroupCreateView': {
        201: 'Grupo creado exitosamente',
        400: 'Datos inválidos para crear grupo',
        403: 'No tienes permiso para crear grupos',
    },
    'MeView': {
        200: 'Perfil obtenido o actualizado exitosamente',
        400: 'Datos inválidos para actualizar perfil',
        401: 'Debes iniciar sesión para ver o actualizar tu perfil',
    },
}