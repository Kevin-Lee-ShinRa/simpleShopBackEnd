from . import views
from rest_framework.routers import DefaultRouter

from .views import StudentViewSet

urlpatterns = []
router = DefaultRouter()
router.register('students', views.StudentViewSet)

urlpatterns += router.urls


