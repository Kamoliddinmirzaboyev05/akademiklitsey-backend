from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Faqat admin rolega ega foydalanuvchilarga ruxsat berish
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_admin_role()
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Adminlar uchun to'liq ruxsat, boshqalar uchun faqat o'qish
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_admin_role()
        )
