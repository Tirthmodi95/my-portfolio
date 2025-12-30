from rest_framework import serializers
from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        if len(data['mobile']) != 10 or not data['mobile'].isdigit():
            raise serializers.ValidationError("Mobile must be 10 digits")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            password=validated_data['password']
        )
        return user