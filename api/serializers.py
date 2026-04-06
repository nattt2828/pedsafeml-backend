from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DetectionEvent, SystemLog, SystemConfig


# ───────── AUTH ─────────

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.CharField(write_only=True, required=False, default='Operator')

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role', 'Operator')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=role
        )
        SystemConfig.objects.create(operator=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'role']

    def get_role(self, obj):
        return obj.first_name if obj.first_name else 'Operator'


# ───────── DETECTIONS ─────────

class DetectionEventSerializer(serializers.ModelSerializer):
    operator_username = serializers.ReadOnlyField(source='operator.username')

    class Meta:
        model = DetectionEvent
        fields = [
            'id',
            'operator_username',
            'status',
            'warning_light',
            'detection_duration',
            'camera_zone',
            'confidence_score',
            'timestamp',
        ]
        read_only_fields = ['id', 'timestamp', 'operator_username']


# ───────── LOGS ─────────

class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = ['id', 'level', 'message', 'camera_zone', 'timestamp']
        read_only_fields = ['id', 'timestamp']


# ───────── CONFIG ─────────

class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = [
            'alert_threshold',
            'sensitivity_mode',
            'confidence_cutoff',
            'camera_zone',
            'notifications_enabled',
            'updated_at',
        ]
        read_only_fields = ['updated_at']