from rest_framework.permissions import (
    BasePermission
)

class IsTeacherRole(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and
            request.user.role == "TEACHER"
        )
    


class IsAdminRole(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and
            request.user.role == "ADMIN"
        )