from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CountryViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'countries', CountryViewSet)

urlpatterns = router.urls
