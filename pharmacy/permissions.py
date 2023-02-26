from rest_framework.permissions import DjangoModelPermissions


class IsCMS(DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser