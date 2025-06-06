# api/renderers.py
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.utils.module_loading import import_string
from django.apps import apps

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        status_code = response.status_code

        # Obtener mensaje personalizado
        message = self.get_custom_message(status_code, renderer_context)

        # Estructura de la respuesta
        response_dict = {
            'status': 'success' if status_code < 400 else 'error',
            'message': message,
            'data': data if status_code < 400 else None,
            'errors': data if status_code >= 400 else None
        }

        # Sobrescribir con mensaje explícito de la vista si existe
        if hasattr(response, 'custom_message'):
            response_dict['message'] = response.custom_message

        return super().render(response_dict, accepted_media_type, renderer_context)

    def get_custom_message(self, status_code, renderer_context):
        view = renderer_context.get('view')
        if not view:
            return self.get_default_message(status_code, renderer_context)

        # Obtener el nombre de la vista
        view_name = view.__class__.__name__

        # Obtener la app de la vista
        app_label = None
        try:
            module = view.__module__
            app_config = apps.get_containing_app_config(module)
            if app_config:
                app_label = app_config.label
        except AttributeError:
            pass

        # Cargar mensajes personalizados de la app
        if app_label:
            try:
                messages_module = import_string(f'{app_label}.messages.MESSAGES')
                if view_name in messages_module and status_code in messages_module[view_name]:
                    return messages_module[view_name][status_code]
            except (ImportError, AttributeError):
                pass

        # Fallback a mensajes por defecto
        return self.get_default_message(status_code, renderer_context)

    def get_default_message(self, status_code, renderer_context):
        request = renderer_context.get('request')
        path = request.path if request else ''

        if 'token' in path:
            return 'Inicio de sesión exitoso' if status_code < 400 else 'Error en el inicio de sesión'
        elif 'users' in path:
            return 'Usuarios obtenidos correctamente' if status_code < 400 else 'Error al obtener usuarios'

        messages = {
            status.HTTP_200_OK: 'Operación completada correctamente',
            status.HTTP_201_CREATED: 'Recurso creado correctamente',
            status.HTTP_204_NO_CONTENT: 'Recurso eliminado correctamente',
            status.HTTP_400_BAD_REQUEST: 'Datos inválidos',
            status.HTTP_401_UNAUTHORIZED: 'No autorizado',
            status.HTTP_403_FORBIDDEN: 'Acceso denegado',
            status.HTTP_404_NOT_FOUND: 'Recurso no encontrado',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Error interno del servidor',
        }
        return messages.get(status_code, 'Operación completada')