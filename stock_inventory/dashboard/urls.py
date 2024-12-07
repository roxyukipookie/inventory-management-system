from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('export/products/', views.export_products, name='export_products'),
    path('role-management/', views.role_management_view, name='role_management_view'),
    path('user-management/', views.user_management_view, name='user_management_view'),
    path('logout/', views.logout_view, name='logout'),
    path('add-user/', views.add_user, name='add_user'),
    path('delete-user/', views.delete_user_view, name='delete_user_view'),
]