from django.urls import path
from . import views

#  test for jwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup', views.SignUp_User_Creation.as_view()),
    path('login', views.Login.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('access_token', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user_details', views.user_details.as_view()),
    path('friend_search', views.friend_search.as_view()),
    path('add_friend', views.add_friend.as_view()),
    path('cancel_request', views.cancel_request.as_view()),
    path('accept_request', views.accept_request.as_view()),
    path('deny_request', views.deny_request.as_view()),
    path('unfriend', views.unfriend.as_view())

]
