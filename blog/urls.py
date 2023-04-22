from .views import BlogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('blog', BlogViewSet, basename='blog')
url_patterns = router.urls
