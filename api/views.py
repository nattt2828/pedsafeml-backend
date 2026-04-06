from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DetectionEvent, SystemLog, SystemConfig
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    DetectionEventSerializer,
    SystemLogSerializer,
    SystemConfigSerializer,
)

# ───────── AUTH ─────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Account created',
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=401)

    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        'user': UserSerializer(user).data,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


# ───────── DETECTIONS ─────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def detection_events(request):
    if request.method == 'GET':
        events = DetectionEvent.objects.all()[:50]
        serializer = DetectionEventSerializer(events, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DetectionEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(operator=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_detection(request):
    event = DetectionEvent.objects.first()
    if not event:
        return Response({'message': 'No data'}, status=404)
    serializer = DetectionEventSerializer(event)
    return Response(serializer.data)


# ───────── LOGS ─────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def system_logs(request):
    if request.method == 'GET':
        logs = SystemLog.objects.all()[:100]
        serializer = SystemLogSerializer(logs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SystemLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(operator=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ───────── CONFIG ─────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def system_config(request):
    config, created = SystemConfig.objects.get_or_create(operator=request.user)

    if request.method == 'GET':
        serializer = SystemConfigSerializer(config)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SystemConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Saved', 'config': serializer.data})
        return Response(serializer.errors, status=400)