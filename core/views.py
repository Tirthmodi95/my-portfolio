from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser, ActivityLog
from .serializers import SignupSerializer

from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'Bunny@@1295')
        return HttpResponse("Admin user created successfully!")
    return HttpResponse("Admin user already exists.")

# ==========================
# Frontend Page
# ==========================
@ensure_csrf_cookie
def home(request):
    return render(request, "index.html")


# ==========================
# Signup API
# ==========================
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            ActivityLog.objects.create(
                username=user.username,
                action="Signed up"
            )
            return Response(
                {"message": "Account created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================
# Login API
# ==========================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Both username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"error": "Account is disabled"},
                status=status.HTTP_403_FORBIDDEN
            )

        login(request, user)

        ActivityLog.objects.create(
            username=user.username,
            action="Logged in"
        )

        return Response(
            {
                "message": "Login successful",
                "role": "admin" if user.is_staff or user.is_superuser else "user"
            },
            status=status.HTTP_200_OK
        )


# ==========================
# Logout API
# ==========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    ActivityLog.objects.create(
        username=request.user.username,
        action="Logged out"
    )
    logout(request)
    return Response({"message": "Logged out successfully"})


# ==========================
# Admin: Get Users
# ==========================
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_users(request):
    users = CustomUser.objects.all()

    data = []
    for user in users:
        data.append({
            "username": user.username,
            "email": user.email,
            "mobile": user.mobile,
            "signup_date": user.signup_date.strftime("%d %b %Y at %I:%M %p")
            if user.signup_date else "N/A"
        })

    return Response({
        "users": data,
        "total": len(data)
    })


# ==========================
# Admin: Activity Logs
# ==========================
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_activity_logs(request):
    logs = ActivityLog.objects.all().order_by("-timestamp")

    data = []
    for log in logs:
        data.append({
            "username": log.username,
            "action": log.action,
            "timestamp": log.timestamp.strftime("%d %b %Y at %I:%M %p")
        })

    return Response({"logs": data})


# ==========================
# Admin: Reset User Password
# ==========================
@api_view(["POST"])
@permission_classes([IsAdminUser])
def reset_user_password(request):
    username = request.data.get("username")
    new_password = request.data.get("new_password")

    if not username or not new_password:
        return Response(
            {"error": "Username and new password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        ActivityLog.objects.create(
            username="Admin",
            action=f"Reset password for {username}"
        )

        return Response(
            {"message": f"Password reset successfully for {username}"}
        )

    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# ==========================
# Admin: Delete User
# ==========================
@api_view(["POST"])
@permission_classes([IsAdminUser])
def delete_user(request):
    username = request.data.get("username")

    if not username:
        return Response(
            {"error": "Username required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(username=username)
        user.delete()

        ActivityLog.objects.create(
            username="Admin",
            action=f"Deleted user {username}"
        )

        return Response({"message": f"User {username} deleted successfully"})

    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model

def setup_database(request):
    if request.method == "GET":
        try:
            # First create migrations for core
            call_command('makemigrations', 'core', verbosity=0)

            # Then apply migrations
            call_command('migrate', verbosity=0)

            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'Bunny@@1295')
                return HttpResponse("<h2>SUCCESS!</h2>Migrations applied and admin user created.<br><br>Go to <a href='/'>login page</a> and use:<br><b>Username: admin</b><br><b>Password: Bunny@@1295</b>")
            return HttpResponse("<h2>Success!</h2>Migrations applied. Admin user already exists.<br><br><a href='/'>Go to login</a>")
        except Exception as e:
            return HttpResponse(f"<h2>Error:</h2> {str(e)}<br><br>Check Render logs for details.")
    return HttpResponse("Visit this URL once to setup the database.")