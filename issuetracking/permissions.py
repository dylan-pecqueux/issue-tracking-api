from .models import Issue, Project, Contributor
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsContributorPermission(BasePermission):
    message = 'Access not allowed ! Only contributors of the project can access'

    def has_object_permission(self, request, view, obj):
        in_project = Contributor.objects.filter(project=obj, user=request.user)
        return len(in_project) != 0


class IsAuthorPermission(BasePermission):
    message = 'Access not allowed ! Only the author can access'

    def has_object_permission(self, request, view, obj):
        is_author = Contributor.objects.get(project=obj, user=request.user)
        return is_author.role == 'author'