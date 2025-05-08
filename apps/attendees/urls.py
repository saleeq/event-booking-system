from rest_framework.routers import DefaultRouter
from .views import AttendeeViewSet

router = DefaultRouter()
router.register(r'', AttendeeViewSet)

urlpatterns = router.urls