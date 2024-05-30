from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User

class SignupView(APIView):
    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        name = request.data.get('name')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=email,email=email, password=password,first_name = name)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if query:
            return User.objects.filter(Q(email__icontains=query) | Q(first_name__icontains=query))
        return User.objects.none()

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)
        from_user = User.objects.get(id=request.user.id)

        if from_user == to_user:
            return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, timestamp__gt=timezone.now()-timezone.timedelta(minutes=1)).count() >= 3:
            return Response({'error': 'Cannot send more than 3 friend requests within a minute'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user, status='pending')
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        friend_request = FriendRequest.objects.get(id=pk)
        request_status = request.data.get('status')
        if friend_request.from_user != User.objects.get(id = request.user.id):
            return Response({'error': 'Cannot respond to friend request not addressed to you'}, status=status.HTTP_400_BAD_REQUEST)

        if request_status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.status = request_status
        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data)


class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        friend_ids = FriendRequest.objects.filter(
            from_user=self.request.user,
            status='accepted'
        ).values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=friend_ids)

class PendingFriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user, status='pending')
