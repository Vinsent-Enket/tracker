from rest_framework.permissions import BasePermission


class IsPublic(BasePermission):
    """ Если в объекте есть пометка о публичном доступе
    """

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True


class IsProprietor(BasePermission):
    """Если создатель объекта соответствует пользователю"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.proprietor


class IsTrueUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj
