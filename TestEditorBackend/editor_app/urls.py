from rest_framework.routers import DefaultRouter

from .views import TestViewSet, HashTagViewSet

router = DefaultRouter()
router.register('editor', TestViewSet)
router.register('hashtags', HashTagViewSet, basename='hashtag')
urlpatterns = router.urls

