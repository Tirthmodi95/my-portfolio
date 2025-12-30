from django.urls import path
from .views import home, SignupView, LoginView, get_users, get_activity_logs, reset_user_password
from .views import get_users, get_activity_logs

urlpatterns = [
    path('', home, name='home'),
    path('api/signup/', SignupView.as_view(), name='api_signup'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/admin/users/', get_users, name='api_admin_users'),
    path('api/admin/logs/', get_activity_logs, name='api_admin_logs'),
    path('api/admin/reset-password/', reset_user_password, name='api_reset_password'),
]
