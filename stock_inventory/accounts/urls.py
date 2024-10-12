from django.urls import path
from .views import signup, login_view, dashboard_view
from . import views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'), 
]
