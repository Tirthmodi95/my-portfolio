from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # your existing paths
    path('', home, name='home'),
    path('api/signup/', SignupView.as_view(), name='api_signup'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/admin/users/', get_users, name='api_admin_users'),
    path('api/admin/logs/', get_activity_logs, name='api_admin_logs'),
    path('api/admin/reset-password/', reset_user_password, name='api_reset_password'),
]

# Serve static files in development AND production
if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)