from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from .models import CustomUser, ActivityLog
from .serializers import SignupSerializer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Get all users for admin panel
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = CustomUser.objects.all().values('username', 'email', 'mobile', 'signup_date')
    users_list = list(users)
    for user in users_list:
        user['signup_date'] = user['signup_date'].strftime('%d %b %Y at %I:%M %p') if user['signup_date'] else 'N/A'
    return Response({"users": users_list, "total": len(users_list)})

# Get activity logs
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_activity_logs(request):
    logs = ActivityLog.objects.all().order_by('-timestamp').values('username', 'action', 'timestamp')
    logs_list = list(logs)
    for log in logs_list:
        log['timestamp'] = log['timestamp'].strftime('%d %b %Y at %I:%M %p')
    return Response({"logs": logs_list})

# Home view - renders your login page
def home(request):
    return render(request, 'index.html')

# Signup API
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            ActivityLog.objects.create(username=user.username, action="Signed up")
            return Response({"message": "Account created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)  # Create session
                ActivityLog.objects.create(
                    username=user.username,
                    action="Logged in"
                )

                # Redirect based on role
                if user.is_superuser or user.is_staff:
                    return Response({
                        "message": "Admin login successful",
                        "redirect": "admin"
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "Login successful",
                        "redirect": "dashboard"
                    }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Account is disabled"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def reset_user_password(request):
    username = request.data.get('username')
    new_password = request.data.get('new_password')

    if not username or not new_password:
        return Response({"error": "Username and new password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        ActivityLog.objects.create(username="Admin", action=f"Reset password for {username}")
        return Response({"message": f"Password reset successfully for {username}"}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)