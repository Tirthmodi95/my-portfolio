from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser, ActivityLog
from .serializers import SignupSerializer


# ==========================
# Frontend Page
# ==========================
def home(request):
    return render(request, 'index.html')


# ==========================
# Signup API
# ==========================
@method_decorator(csrf_exempt, name='dispatch')
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
                {"message": "Account created successfully!"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================
# Login API
# ==========================
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Both username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_active:
            return Response(
                {"error": "Account is disabled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        login(request, user)
        ActivityLog.objects.create(
            username=user.username,
            action="Logged in"
        )

        return Response(
            {
                "message": "Login successful",
                "redirect": "admin" if user.is_staff else "dashboard"
            },
            status=status.HTTP_200_OK
        )


# ==========================
# Admin APIs
# ==========================
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = CustomUser.objects.all().values(
        'username',
        'email',
        'mobile',
        'signup_date'
    )

    users_list = []
    for user in users:
        users_list.append({
            "username": user["username"],
            "email": user["email"],
            "mobile": user["mobile"],
            "signup_date": user["signup_date"].strftime('%d %b %Y at %I:%M %p')
            if user["signup_date"] else "N/A"
        })

    return Response(
        {
            "users": users_list,
            "total": len(users_list)
        }
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_activity_logs(request):
    logs = ActivityLog.objects.all().order_by('-timestamp')

    logs_list = []
    for log in logs:
        logs_list.append({
            "username": log.username,
            "action": log.action,
            "timestamp": log.timestamp.strftime('%d %b %Y at %I:%M %p')
        })

    return Response({"logs": logs_list})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def reset_user_password(request):
    username = request.data.get('username')
    new_password = request.data.get('new_password')

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
            {"message": f"Password reset successfully for {username}"},
            status=status.HTTP_200_OK
        )

    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
