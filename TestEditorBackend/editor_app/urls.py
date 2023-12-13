from rest_framework.routers import DefaultRouter

from .views import TestViewSet, HashTagViewSet, ProtocolViewSet

router = DefaultRouter()
router.register('editor', TestViewSet)
router.register('hashtags', HashTagViewSet, basename='hashtag')
router.register('protocol', ProtocolViewSet, basename='protocol')
urlpatterns = router.urls

