from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, IssueView, ProjectView, ContributorView, CommentView


router = DefaultRouter()
router.register(r'projects', ProjectView)
router.register(r'projects/(?P<project_id>\d+)/issues', IssueView)
router.register(r'projects/(?P<project_id>\d+)/users', ContributorView)
router.register(r'projects/(?P<project_id>\d+)/issues/(?P<issue_id>\d+)/comments', CommentView)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]