from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

from .views import custom_logout_view

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('export/products/', views.export_products, name='export_products'),
    path('role-management/', views.role_management_view, name='role_management_view'),
    path('user-management/', views.user_management_view, name='user_management_view'),
    path('add-user/', views.add_user, name='add_user'),
    path('delete_users/', views.delete_users, name='delete_users'),
    #path('reset-password/', views.reset_password_view, name='reset_password'),
    path('edit-role/', views.edit_role_view, name='edit_role_view'),
    path('logout/', custom_logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
