from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> Any:
        """cannot view article but cannot edit or delete if not owner"""
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> Any:
        """can only edit and delete own product"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_superuser


class IsInventoryOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> Any:
        """cannot view article but cannot edit or delete if not owner"""
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> Any:
        """can only edit and delete own inventory"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.product.owner == request.user or request.user.is_superuser
