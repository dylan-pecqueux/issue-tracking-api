from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, IssueView, ProjectDetailView


router = DefaultRouter()
router.register(r'projects', ProjectDetailView)

urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/<int:pk>/issues/', IssueView.as_view()),
]