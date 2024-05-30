from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, LoginView, UserSearchView, FriendRequestView, FriendListView, PendingFriendRequestListView,UserListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-requests/', FriendRequestView.as_view(), name='send_friend_request'),
    path('friend-requests/<int:pk>/', FriendRequestView.as_view(), name='respond_friend_request'),
    path('friends/', FriendListView.as_view(), name='list_friends'),
    path('pending-requests/', PendingFriendRequestListView.as_view(), name='list_pending_requests'),
    path('users/', UserListView.as_view(), name='list_users'),
]
