from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, ProjectView, IssueView, ProjectDetailView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('project/', ProjectView.as_view()),
    path('project/<int:pk>/', ProjectDetailView.as_view()),
    path('project/<int:pk>/issues/', IssueView.as_view()),
]