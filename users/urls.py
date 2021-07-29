from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from users.views import *

route = routers.DefaultRouter()
route.register('users/address', AddressViewSet, basename='address')

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('activate/', activate_user_account, name='activate_user'),
    path('me/', ListUserView.as_view(), name='list_user'),
    path('update/', update_user, name='update_user'),
    path('update/password/', update_user_password, name='update_user_password'),
    path('forget-password/', forget_password, name='forget_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('delete/', delete_user_account, name='delete_user_account'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

