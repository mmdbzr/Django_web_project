from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "resume", "avatar", "avatar_thumbnail"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "profile"]
        read_only_fields = ["id", "profile"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def validate_role(self, value):
        """
        نقش باید یکی از سه مقدار مجاز باشه
        """
        if value not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Role must be seeker, employer, or admin.")
        return value

    def create(self, validated_data):
        """
        ساخت کاربر جدید با پسورد هش‌شده و پروفایل
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False  # تا تایید ایمیل فعال نشه
        user.save()

        # ایجاد پروفایل مرتبط
        UserProfile.objects.get_or_create(user=user)

        return user
