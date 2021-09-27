from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, IssueView, ProjectView


router = DefaultRouter()
router.register(r'projects', ProjectView)
router.register(r'projects/(?P<pk>\d+)/issues', IssueView)

urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]