from rest_framework.permissions import BasePermission

class HasPermissionCodename(BasePermission):
    codename = ''  # por defecto; cada vista puede sobreescribir esto

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        codename = getattr(view, 'permission_codename', self.codename)
        return request.user.has_perm(codename)