from rest_framework.routers import DefaultRouter

from .views import TestViewSet

router = DefaultRouter()
router.register('', TestViewSet)

urlpatterns = router.urls

