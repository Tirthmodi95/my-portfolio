from django.contrib import admin
from django.urls import path

from core.views import (
    home,
    SignupView,
    LoginView,
    logout_view,
    delete_user,
    get_users,
    get_activity_logs,
    reset_user_password,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend
    path('', home, name='home'),

    # Auth APIs
    path('api/signup/', SignupView.as_view(), name='api_signup'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', logout_view, name='api_logout'),

    # Admin APIs
    path('api/admin/users/', get_users, name='api_admin_users'),
    path('api/admin/logs/', get_activity_logs, name='api_admin_logs'),
    path('api/admin/reset-password/', reset_user_password, name='api_reset_password'),
    path('api/admin/delete-user/', delete_user, name='api_delete_user'),
]
