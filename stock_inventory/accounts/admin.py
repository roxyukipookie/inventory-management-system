from django.contrib import admin
from .models import CustomUser, Role, UserProfile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'role__name')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active', 'role__name')  # Add a filter for roles
    ordering = ('email',)

    # Custom queryset for staff and owner/admin roles
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Show all users to superusers
        elif request.user.groups.filter(name='staff').exists():
            return qs.filter(role__name='staff')
        elif request.user.groups.filter(name='owner').exists():
            return qs.filter(role__name__in=['owner', 'admin'])
        return qs

# Register CustomUser with a single admin
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'additional_info')
