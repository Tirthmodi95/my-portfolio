from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import your views from the core app
from core.views import (
    home,
    SignupView,
    LoginView,
    get_users,
    get_activity_logs,
    reset_user_password,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/signup/', SignupView.as_view(), name='api_signup'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/admin/users/', get_users, name='api_admin_users'),
    path('api/admin/logs/', get_activity_logs, name='api_admin_logs'),
    path('api/admin/reset-password/', reset_user_password, name='api_reset_password'),
]

# Serve static files in both development and production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)