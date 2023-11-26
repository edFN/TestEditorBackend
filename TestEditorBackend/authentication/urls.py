

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from .views import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet,basename='user')

urlpatterns = router.urls + [
    path('login', TokenObtainPairView.as_view(), name='token_create'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify', TokenVerifyView.as_view(), name='token_verify'),
]