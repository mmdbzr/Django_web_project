from rest_framework import serializers
from .models import Job, Application


# -------------------------
# Job Serializer (CRUD)
# -------------------------
class JobSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # نمایش username کارفرما
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)  # ID کارفرما برای راحتی

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'location',
            'salary',
            'is_active',
            'created_at',
            'updated_at',
            'user',
            'user_id',
        ]


# -------------------------
# Application Serializer (Read)
# -------------------------
class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    job = serializers.StringRelatedField(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job', 'job_id',
            'user', 'user_id',
            'resume',
            'status',
            'created_at'
        ]


# -------------------------
# Application Create Serializer (Write)
# -------------------------
class ApplicationCreateSerializer(serializers.ModelSerializer):
    """
    این سریالایزر برای درخواست اپلای استفاده میشه.
    فقط job و resume از کاربر گرفته میشه،
    user به صورت خودکار از request تعیین میشه.
    """
    class Meta:
        model = Application
        fields = ['job', 'resume']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)