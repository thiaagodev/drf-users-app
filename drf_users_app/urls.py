from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.urls import route as users_route

router = routers.DefaultRouter()
router.registry.extend(users_route.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
]
